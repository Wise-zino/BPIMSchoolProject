import csv
import os

class PersonalManager:
    def __init__(self):
        self.contacts_file = 'contacts.csv'
        self.tasks_file = 'tasks.txt'
        self.contacts = []
        self.next_id = 1
        self.load_contacts()
        
    def load_contacts(self):
        """ Loads contacts from the CSV file into memory on startup """
        if not os.path.exists(self.contacts_file):
            # Create file with headers if it doesn't exist
            with open(self.contacts_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'phone', 'email'])
        else:
            with open(self.contacts_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader, None) # Skip the header row
                for row in reader:
                    if row: # Avoid empty lines
                        contact = [int(row[0]), row[1], row[2], row[3]]
                        self.contacts.append(contact)
                        if contact[0] >= self.next_id:
                            self.next_id = contact[0] + 1

    def save_contacts(self):
        """ Saves the current list of contacts back to the CSV file """
        with open(self.contacts_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'phone', 'email'])
            for contact in self.contacts:
                writer.writerow(contact)

    def add_contact(self, name=False, email=False, phone_no=False):
        """ a method for adding contacts """
        try:
            if (not name and not email and not phone_no):
                return False, "All contacts field required"
            
            new_contact = [self.next_id, name, phone_no, email]
            self.contacts.append(new_contact)
            self.next_id += 1
            self.save_contacts()
            
            return True, f"successfully added contact({name})"
        except Exception as e:
            return False, str(e)
    
    def get_all_contact(self):
        """ get contacts """
        try:
            return True, self.contacts
        except Exception as e:
            return False, str(e)
    
    def search_contact(self, name):
        """ search for a particular contact by name """
        try:
            # Performs a case-insensitive search 
            results = [c for c in self.contacts if name.lower() in c[1].lower()]
            return True, results
        except Exception as e:
            return False, str(e)
    
    def update_contact(self, field, contact_id, value):
        """ update a particular contact """
        try:
            for c in self.contacts:
                if c[0] == int(contact_id):
                    if field == 1:
                        c[1] = value # Update Name
                    elif field == 2:
                        c[3] = value # Update Email (Index 3)
                    elif field == 3:
                        c[2] = value # Update Phone (Index 2)
                    
                    self.save_contacts()
                    return True, 'Contact updated'
            return False, 'Contact not found'
        except Exception as e:
            return False, str(e)
    
    def delete_contact(self, contact_id):
        """ delete a particular contact """
        try:
            initial_len = len(self.contacts)
            self.contacts = [c for c in self.contacts if c[0] != int(contact_id)]
            
            if len(self.contacts) < initial_len:
                self.save_contacts()
                return True, 'Contact deleted'
            return False, 'Contact not found'
        except Exception as e:
            return False, str(e)

    def add_task(self, task):
        """ Adds a daily task to a txt file """
        try:
            with open(self.tasks_file, mode='a') as file:
                file.write("- " + task + "\n")
            return True, "Task added successfully to your diary"
        except Exception as e:
            return False, str(e)

    def view_tasks(self):
        """ Views daily tasks from the txt file """
        try:
            if not os.path.exists(self.tasks_file):
                return True, []
            with open(self.tasks_file, mode='r') as file:
                tasks = file.readlines()
            return True, [t.strip() for t in tasks if t.strip()]
        except Exception as e:
            return False, str(e)

    def display_prompt(self):
        print("\nENTER REQUEST-NO TO SELECT A REQUEST")
        print("1. Add a contact")
        print("2. Get all contacts")
        print("3. Search for a contact")
        print("4. Update a contact")
        print("5. Delete a contact")
        print("6. Add a daily task")
        print("7. View daily tasks")
        print("8. Exit program")


# START PROGRAM
manager = PersonalManager()

print("-----PERSONAL INFORMATION MANAGEMENT SYSTEM [GROUP 1]-----")

user_request = None
while user_request != '8' and user_request != 'exit':
    manager.display_prompt()
    user_request = input("enter here: ")
    
    if user_request == str(1):
        contact_name = input('Enter the name of your new contact: ')
        contact_phone_no = input('Enter the phone number of your new contact: ')
        contact_email = input('Enter the email of your new contact: ')
        
        while not (contact_name and contact_phone_no and contact_email):
            print('\nplease enter all fields')
            contact_name = input('Enter the name of your new contact: ')
            contact_phone_no = input('Enter the phone number of your new contact: ')
            contact_email = input('Enter the email of your new contact: ')
        
        response, message = manager.add_contact(contact_name, contact_email, contact_phone_no)
        print(message if response else '\nThere was an error adding your contact, please try again')
    
    elif user_request == str(2):
        response, all_contacts = manager.get_all_contact()
        
        if response:
            if not all_contacts:
                print("No contacts saved yet.")
            else:
                i = 1
                for contact in all_contacts:
                    print(f'{i}.')
                    print(f'   name: {contact[1]}')
                    print(f'   phone number: {contact[2]}')
                    print(f'   email: {contact[3]}')
                    print()
                    i += 1
        else:
            print('\nThere was an error getting your contacts, please try again')
    
    elif user_request == str(3):
        contact_name = input("Enter contact's name: ")
        
        while not contact_name:
            print('Please enter the contact name')
            contact_name = input("Enter contact's name: ")
            
        response, result = manager.search_contact(contact_name)
        
        if response:
            i = 1
            if result:
                print(f'\nRESULTS FOR "{contact_name}"')
                for contact in result:
                    print(f'{i}.')
                    print(f'   name: {contact[1]}')
                    print(f'   phone number: {contact[2]}')
                    print(f'   email: {contact[3]}')
                    print()
                    i += 1
            else:
                print(f'\nNO CONTACT FOUND WITH NAME - "{contact_name}"')
        else:
            print('\nThere was an error searching your contacts, please try again')
    
    elif user_request == str(4):
        print('\nAll contacts')
        response, result = manager.get_all_contact()
        if response and result:
            contact_list = []
            i = 1
            for contact in result:
                contact_list.append(contact)
                print(f'{i}.')
                print(f'   name: {contact[1]}')
                print(f'   phone number: {contact[2]}')
                print(f'   email: {contact[3]}')
                print()
                i += 1
                
            serial_no = input('enter the serial-number of the one you wish to update (or 0 to cancel): ')
            
            if serial_no != '0' and serial_no.isdigit() and int(serial_no) <= len(contact_list):
                print('\nWhat would you like to update ?')
                print('1. NAME')
                print('2. EMAIL')
                print('3. PHONE NUMBER')
                
                update_field = input('enter here: ')
                
                if update_field == str(1) or update_field.lower() == 'name':
                    value = input('\nenter new name: ')
                    response, message = manager.update_contact(1, contact_list[int(serial_no)-1][0], value)
                    print(message)
                elif update_field == str(2) or update_field.lower() == 'email':
                    value = input('\nenter new email: ')
                    response, message = manager.update_contact(2, contact_list[int(serial_no)-1][0], value)
                    print(message)
                elif update_field == str(3) or update_field.lower() == 'phone number':
                    value = input('\nenter new phone number: ')
                    response, message = manager.update_contact(3, contact_list[int(serial_no)-1][0], value)
                    print(message)
                else:
                    print('invalid update field')
            else:
                print('Update cancelled or invalid number.')
        else:
            print('No contacts available to update.')
                
    elif user_request == str(5):
        print('\nAll contacts')
        response, result = manager.get_all_contact()
        if response and result:
            contact_list = []
            i = 1
            for contact in result:
                contact_list.append(contact)
                print(f'{i}.')
                print(f'   name: {contact[1]}')
                print(f'   phone number: {contact[2]}')
                print(f'   email: {contact[3]}')
                print()
                i += 1
                
            serial_no = input('enter the serial-number of the one you wish to delete (or 0 to cancel): ')
            
            if serial_no != '0' and serial_no.isdigit() and int(serial_no) <= len(contact_list):
                print('This contact details will be permanently deleted')
                print(f'NAME: {contact_list[int(serial_no)-1][1]}')
                print(f'PHONE NUMBER : {contact_list[int(serial_no)-1][2] }')
                print(f'EMAIL: {contact_list[int(serial_no)-1][3]}')
                print()
                
                delete_response = input('Confirm delete(y/n): ')
                if delete_response.lower() in ['y', 'yes']:
                    response, message = manager.delete_contact(contact_list[int(serial_no)-1][0])
                    print(message)
                else:
                    print("Deletion cancelled.")
            else:
                print('Deletion cancelled or invalid number.')
        else:
            print("No contacts available to delete.")

    elif user_request == str(6):
        task_text = input("Enter your new daily task: ")
        if task_text:
            response, message = manager.add_task(task_text)
            print(message)
        else:
            print("Task cannot be empty.")

    elif user_request == str(7):
        response, tasks = manager.view_tasks()
        if response:
            if not tasks:
                print("\nYou have no daily tasks saved yet.")
            else:
                print("\nYOUR DAILY TASKS:")
                for i, task in enumerate(tasks, 1):
                    print(task)
        else:
            print("\nError fetching tasks.")
                
    elif user_request == str(8) or user_request.lower() == 'exit':
        print('\nNOW EXITING PROGRAM. All data has been saved to contacts.csv and tasks.txt.')
        break
    
    else:
        print("\nInvalid input, please try again.")
