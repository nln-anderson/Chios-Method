# Implementing the calculator with a GUI
# Uses the MVC model

from typing import Tuple
import customtkinter as ctk
import numpy as np

class ChioModel:
    """
    Handles the backend operations of the calculator. Contains the functions needed to calculate the determinant.
    """

    # Constructor
    def __init__(self) -> None:
        pass

    # Methods
    def two_by_two_determinant(self, a: float,b: float,c: float,d: float) -> float:
        """
        Calculates the determinant of a 2x2 matrix. 

        PARAMETERS:
        a,b,c,d (type: float) - the entries of a 2x2 matrix

        OUTPUT:
        determinant (type: float) - the determinant of the 2x2 matrix

        DOCTESTS:
        >>> m = ChioModel()
        >>> m.two_by_two_determinant(2,3,4,5)
        -2
        """

        determinant = a * d - c * b

        return determinant

    def Chios_Matrix(self, matrix: np.ndarray) -> np.ndarray:
        """
        Creates Chio's Matrix of a given matrix input.

        PARAMETERS:
        matrix (type: array) - an nxn matrix

        OUTPUT:
        c_matrix (type: array) - Chio's matrix, an (n-1) x (n-1) matrix 

        DOCTESTS:
        >>> m = ChioModel()
        >>> mat = m.Chios_Matrix(np.array([[2,1,1], [3,4,-1], [1,5,1]]))
        >>> print(mat)
        [[ 5. -5.]
         [ 9.  1.]]
        """
        # Establish matrix dimensions
        n = len(matrix)

        # Create an empty matrix that will be filled with Chio determinants
        c_matrix = np.zeros((n-1, n-1))

        # Filling the entries
        for i in range(n-1):
            # For each row
            for j in range(n-1):
                # For each entry in the row (aka column), compute the corresponding 2x2 determinant
                c_matrix[i, j] = self.two_by_two_determinant(matrix[0,0], matrix[0,j + 1], matrix[i + 1,0], matrix[i + 1,j+1])
            
        return c_matrix

    def determinant_calculator_chio(self, matrix: np.ndarray) -> float:
        """
        Calculates the determinant of an n x n matrix using Chio's Method

        PARAMETERS:
        matrix (type: arrary) - an n x n matrix

        OUTPUT:
        determinant (type: float) - the determinant of the matrix

        DOCTESTS:
        >>> m = ChioModel()
        >>> m.determinant_calculator_chio(np.array([[2,1,1], [3,4,-1], [1,5,1]]))
        25.0
        """
        n = len(matrix)

        # Base Case
        if n == 1:
            return matrix[0][0]
        
        # Chio's Method
        else:
            
            c_matrix = self.Chios_Matrix(matrix)
            
            return self.determinant_calculator_chio(c_matrix) / ((matrix[0][0])**(n-2))

class ChioView(ctk.CTkFrame):
    """
    Handles the GUI for the calculator
    """
    # Instance vars (they are things that need to be accessible by controller)
    mat_frame: ctk.CTkFrame # This starts as empty frame, but updates to a frame once the confirm button is pressed
    dim_entry: ctk.CTkEntry
    entry_widgets: list[list[ctk.CTkEntry]] # Matrix entries used in model
    result_lab: ctk.CTkLabel
    calc_det_but: ctk.CTkButton

    # Constructor
    def __init__(self, parent: ctk.CTk, model: ChioModel) -> None:
        super().__init__(parent)
        self.model = model
        self.mat_frame = ctk.CTkFrame(self)
        self.entry_widgets = []
        self.create_ui()

    # Methods
    def create_ui(self) -> None:
        # Create the top frame, mat frame, and bottom frame and pack it
        dim_frame = ctk.CTkFrame(self)
        dim_frame.pack(side= "top")

        self.mat_frame.pack(side= "top")

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(side= "top")

        # Create the widgets wihtin the frame
        # Top
        dim_label = ctk.CTkLabel(dim_frame, text="Dimension of Matrix:")
        dim_entry = ctk.CTkEntry(dim_frame)
        confirm_but = ctk.CTkButton(dim_frame, text= "Confirm", command=self.set_dim)
        # Bottom
        calc_det_but = ctk.CTkButton(bottom_frame, text="Calculate Determinant", command= self.calculate_det)
        result_lab = ctk.CTkLabel(bottom_frame, text="Select size, fill entries, hit calculate")

        # Make sure that entry and lable are assigned as instance vars
        self.dim_entry = dim_entry
        self.result_lab = result_lab
        self.calc_det_but = calc_det_but

        # Packing them within the frame
        # Top
        dim_label.pack(side= "left")
        dim_entry.pack(side= "left")
        confirm_but.pack(side= "left")
        # Bottom
        calc_det_but.pack(side= "left")
        result_lab.pack(side= "left")
    
    def set_dim(self) -> None:
        """
        When the confirm button is pressed, create the matrix layout.
        """
        dimension = int(self.dim_entry.get())  # Get the dimension from the entry
        self.set_mat(dimension)
    
    def calculate_det(self):
        """
        Use the model to find the determinant and update the result label with the result.
        """
        # Get matrix entries from the view
        matrix_entries = []
        for row in self.entry_widgets:
            row_list = []
            for entry in row:
                row_list.append(float(entry.get()))
            matrix_entries.append(row_list)

        # Create an np array to run the calculation
        matrix = np.array(matrix_entries)

        # Calculate determinant with the model
        det = self.model.determinant_calculator_chio(matrix)
        print(det)

        self.result_lab.configure(text = f"Determinant: {det}")

    def set_mat(self, dim: int) -> None:
        """
        Creates the matrix entries within the mat_frame based on the dimension in the entry box.
        """

        # Clear anything in the mat_frame
        for widget in self.mat_frame.winfo_children():
            widget.destroy()

        # Clear existing entry widgets
        self.entry_widgets.clear()

        # Create the matrix of entry boxes
        for i in range(dim):
            row_widgets = []  # To store widgets in each row
            for j in range(dim):
                entry = ctk.CTkEntry(self.mat_frame)
                entry.grid(row=i, column=j)
                row_widgets.append(entry)  # Append entry widget to row_widgets
            self.entry_widgets.append(row_widgets)  # Append row_widgets to entry_widgets

        # Pack the matrix frame
        self.mat_frame.pack(side="top")


class ChioController:
    """
    Connects the view and model and handles communication between the two.
    """
    # Instance vars
    model: ChioModel
    view: ChioView

    # Constructor
    def __init__(self, model: ChioModel, view: ChioView) -> None:
        self.model = model
        self.view = view
        self.set_button()

    def set_button(self):
        """
        Sets the command of the calculate button within the view.
        """
        
        self.view.calc_det_but["command"] = self.calculate_det

    def calculate_det(self):
        """
        Use the model to find the determinant and update the result label with the result.
        """
        # Get matrix entries from the view
        matrix_entries = []
        for row in self.view.entry_widgets:
            row_list = []
            for entry in row:
                row_list.append(float(entry.get()))
            matrix_entries.append(row_list)

        # Create an np array to run the calculation
        matrix = np.array(matrix_entries)

        # Calculate determinant with the model
        det = self.model.determinant_calculator_chio(matrix)

        self.view.result_lab.config(text=f"Determinant: {det}")

def main():
    """
    Connects the pieces to run the app.
    """
    # Create the window where we place the app
    window = ctk.CTk()

    # Create the MVC
    m = ChioModel()
    v = ChioView(window, m)

    # Pack the view
    v.pack(side= "top")

    window.mainloop()

main()



    






