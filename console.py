#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User

class DailyDriveCommand(cmd.Cmd):
    """
    Command interpreter for the DailyDrive application.
    Implements basic commands and operations for the models.
    """
    prompt = "(DailyDrive) "
    classes = storage.classes

    def do_create(self, arg):
        """Creates a new instance of a class, saves it, and prints the id."""
        if not arg:
            print("** class name missing **")
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = self.classes[arg]()
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
            count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == arg)
            print(count)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or updating attribute.
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

    def do_update_dict(self, arg):
        """
        Updates an instance based on the class name and id with a dictionary.
        Usage: update_dict <class name> <id> <dictionary representation>
        """
        args = arg.split(maxsplit=2)
        if len(args) < 2:
            print("** class name missing **" if len(args) < 1 else "** instance id missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 2:
            print("** dictionary representation missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                obj = storage.all()[key]
                try:
                    update_dict = eval(args[2])
                except SyntaxError:
                    print("** invalid dictionary representation **")
                    return

                if not isinstance(update_dict, dict):
                    print("** dictionary representation missing **")
                    return

                for attr_name, attr_value in update_dict.items():
                    if attr_name in ["id", "created_at", "updated_at"]:
                        continue
                    # Type casting the attribute value
                    if isinstance(attr_value, str):
                        if attr_value.isdigit():
                            attr_value = int(attr_value)
                        else:
                            try:
                                attr_value = float(attr_value)
                            except ValueError:
                                pass
                    setattr(obj, attr_name, attr_value)
                obj.save()

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """
        Overrides the default behavior of repeating the last command when an empty line is entered.
        """
        pass

    def preloop(self):
        """Initialize class storage."""
        storage.reload()

    def postloop(self):
        """Save storage state before quitting."""
        storage.save()

if __name__ == '__main__':
    DailyDriveCommand().cmdloop()
