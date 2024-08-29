#!/usr/bin/python3
import re
import cmd
from models.base_model import BaseModel
from models import storage

class DailyDriveCommand(cmd.Cmd):
    """
    Command interpreter for the DailyDrive application.
    Implements basic commands and operations for the models.
    """
    prompt = "(DailyDrive) "

    def __init__(self):
        super().__init__()
        storage.reload()  # Load the storage
        self.classes = storage.classes  # Set classes to the loaded dictionary

    def parse_params(self, params):
        """Parses parameters in the format key=value."""
        parsed = {}
        for param in params:
            key_value = param.split('=', 1)
            if len(key_value) != 2:
                continue

            key = key_value[0].strip()
            value = key_value[1].strip()

            # Remove surrounding quotes and escape backslashes in strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('\\"', '"').replace('_', ' ')
            else:
                # Convert value to float or int if applicable
                if re.match(r"^\d+\.\d+$", value):
                    value = float(value)
                elif value.isdigit():
                    value = int(value)

            parsed[key] = value
        return parsed

    def do_create(self, arg):
        """Creates a new instance of a class with given parameters, saves it, and prints the id."""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        # Create a new instance of the class
        try:
            new_instance = self.classes[class_name]()
        except Exception as e:
            print(f"** error creating instance: {e} **")
            return

        # Parse parameters
        params = self.parse_params(args[1:])
        for key, value in params.items():
            setattr(new_instance, key, value)

        # Save and print the id
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            obj = storage.all().get(key)
            if obj:
                print(obj)
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            obj = storage.all().pop(key, None)
            if obj:
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representations of all instances or instances of a specific class."""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
        else:
            result = []
            for obj in storage.all().values():
                if not arg or obj.__class__.__name__ == arg:
                    result.append(str(obj))
            print(result)

    def do_count(self, arg):
        """Counts the number of instances of a class."""
        if not arg:
            print("** class name missing **")
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            count = sum(1 for obj in storage.all().values()
                        if obj.__class__.__name__ == arg)
            print(count)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            obj = storage.all().get(key)
            if obj:
                attr_name = args[2]
                attr_value = args[3].strip('"')

                # Type casting the attribute value
                if attr_value.isdigit():
                    attr_value = int(attr_value)
                else:
                    try:
                        attr_value = float(attr_value)
                    except ValueError:
                        pass

                setattr(obj, attr_name, attr_value)
                obj.save()
            else:
                print("** no instance found **")

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """
        Overrides the default behavior of repeating the last command
        when an empty line is entered.
        """
        pass


if __name__ == '__main__':
    DailyDriveCommand().cmdloop()
