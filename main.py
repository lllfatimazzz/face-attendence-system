"""Main entry point for Face Attendance System"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from database.db_config import DatabaseConfig
from gui.main_window import MainWindow

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Initialize database
    db_config = DatabaseConfig()
    if not db_config.initialize_database():
        QMessageBox.critical(None, "Database Error", 
                           "Failed to initialize database. Please check your MySQL connection settings.")
        sys.exit(1)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

