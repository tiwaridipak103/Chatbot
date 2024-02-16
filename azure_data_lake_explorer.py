import tkinter as tk
from azure.storage.blob import BlobServiceClient

class AzureStorageExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Azure Storage Explorer")

        # Initialize set to store expanded folders
        self.expanded_folders = set()

        # Azure Storage connection
        self.connection_string = "<your-azure-storage-connection-string>"
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Container name
        self.container_name = "<your-container-name>"

        # File list frame
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.file_label = tk.Label(self.file_frame, text="Files:")
        self.file_label.pack()

        self.file_listbox = tk.Listbox(self.file_frame)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        # Bind double-click event to file listbox
        self.file_listbox.bind('<Double-Button-1>', self.on_file_double_click)

        # Populate files
        self.populate_files()

    def populate_files(self, folder_name=None):
        # Clear existing items
        self.file_listbox.delete(0, tk.END)

        # List blobs in container
        container_client = self.blob_service_client.get_container_client(self.container_name)
        blobs = container_client.list_blobs()
        files = []
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) == 1:
                files.append(parts[0])
            elif len(parts) > 1:
                # Check if the blob is in the selected folder or a sub-folder
                if parts[0] == folder_name and len(parts) == 2:
                    files.append(parts[-1])
                elif parts[0] == folder_name:
                    # Skip files in sub-folders
                    continue

        # Check if the folder is already expanded
        if folder_name in self.expanded_folders:
            # If folder is expanded, remove its files from the listbox to collapse it
            self.expanded_folders.remove(folder_name)
        else:
            # If folder is not expanded, add its files to the listbox to expand it
            self.expanded_folders.add(folder_name)
            for file in files:
                self.file_listbox.insert(tk.END, file)

    def on_file_double_click(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            self.populate_files(selected_item)

def main():
    root = tk.Tk()
    app = AzureStorageExplorer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
