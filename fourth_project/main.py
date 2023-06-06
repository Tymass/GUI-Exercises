from PyQt5.QtWidgets import QApplication
from engine import Engine
from visualization import MainWindow
from multiprocessing import Process, freeze_support, Manager


def run_visualization(shared_dict):
    # Create and display the main window
    app = QApplication([])
    window = MainWindow(shared_dict)
    window.show()

    # Run the application
    app.exec_()


if __name__ == "__main__":
    freeze_support()

    manager = Manager()
    # Create a dict in shared memory
    shared_dict = manager.dict()
    engine_1 = Engine(1, shared_dict)

    # Start the engine warm-up in a separate process
    engine_process_warm_up = Process(target=engine_1.engineStart)
    engine_process_warm_up.start()

    # Start the visualization in a separate process
    visualization_process = Process(
        target=run_visualization, args=(engine_1.engine_mode,))
    visualization_process.start()

    # Wait for the first process to finish
    engine_process_warm_up.join()

    # Now that engineStart() has finished, start engineCycle()
    engine_process_cycle = Process(target=engine_1.engineCycle)
    engine_process_cycle.start()

    # Wait for the remaining processes to finish
    engine_process_cycle.join()
    visualization_process.join()
