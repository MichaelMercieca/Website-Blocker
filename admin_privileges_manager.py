import ctypes
import sys


# TODO make multi OS support by making the OS a parameter for all functions
def is_admin_windows():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return False


def run_as_admin_windows():
    """
    Restart the script with administrative privileges if not already running as admin.
    """
    if sys.platform == 'win32': # Check if the script is running on Windows
        if not is_admin_windows():
            print("Requesting administrative privileges...")
            # Collect command-line arguments
            args = sys.argv
            # Convert arguments to a single string
            arg_str = ' '.join(f'"{arg}"' for arg in args)
            try:
                # Attempt to restart the script with elevated privileges
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, arg_str, None, 1)
            except OSError as e:
                # Handle errors related to OS operations
                print(f"OS error occurred: {e}")
            except ctypes.WinError as e:
                # Handle specific errors related to ctypes
                print(f"Error from ctypes: {e}")
            except Exception as e:
                # Catch any other exceptions that may occur
                print(f"Failed to acquire administrative privileges: {e}")
            finally:
                # Ensure the script exits if relaunching
                sys.exit(0)
    else:
        print("Administrative privilege escalation is only implemented for Windows.")
        print("Press Enter to exit:")
        input()
