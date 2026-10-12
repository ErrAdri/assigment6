class EmployeeNode:
    """A single employee in the reporting structure."""

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class TeamTree:
    """Manages the company's reporting hierarchy as a binary tree."""

    def __init__(self):
        self.root = None

    def insert(self, manager_name, employee_name, side, current_node=None):
        """Recursively find manager_name and add employee_name on the given side.

        Returns True if the employee was placed (or the manager was found and an
        error was reported), False if the manager wasn't found in this subtree.
        """
        is_top_call = current_node is None

        # Start the search at the root on the first call.
        if is_top_call:
            if self.root is None:
                print("❌ The tree is empty. Add a team lead first.")
                return False
            current_node = self.root

        side = side.strip().lower()
        if side not in ("left", "right"):
            print(f"❌ '{side}' is not a valid side. Use 'left' or 'right'.")
            return False

        # Found the manager: try to place the new employee.
        if current_node.name == manager_name:
            if getattr(current_node, side) is None:
                setattr(current_node, side, EmployeeNode(employee_name))
                print(f"✅ {employee_name} added to the {side.upper()} of {manager_name}")
            else:
                occupant = getattr(current_node, side).name
                print(f"❌ {manager_name}'s {side.upper()} spot is already taken by {occupant}.")
            return True

        # Not the manager: search the left subtree, then the right subtree.
        found = False
        if current_node.left is not None:
            found = self.insert(manager_name, employee_name, side, current_node.left)
        if not found and current_node.right is not None:
            found = self.insert(manager_name, employee_name, side, current_node.right)

        # Only the top-level call reports a missing manager, so the message prints once.
        if is_top_call and not found:
            print(f"❌ Manager '{manager_name}' was not found in the team.")
        return found

    def print_tree(self, node=None, level=0):
        """Recursively print the team structure with indentation per level."""
        if node is None:
            if level == 0:
                node = self.root
                if node is None:
                    print("(The team is empty.)")
                    return
            else:
                return  # Reached a leaf's empty child.

        print("  " * level + "- " + node.name)

        if node.left is not None:
            self.print_tree(node.left, level + 1)
        if node.right is not None:
            self.print_tree(node.right, level + 1)


def company_directory():
    tree = TeamTree()

    while True:
        print("\n📋 Team Management Menu")
        print("1. Add Team Lead (root)")
        print("2. Add Employee")
        print("3. Print Team Structure")
        print("4. Exit")
        choice = input("Choose an option (1–4): ").strip()

        if choice == "1":
            if tree.root is not None:
                print(f"❌ {tree.root.name} is already the team lead.")
                continue
            name = input("Enter team lead's name: ").strip()
            tree.root = EmployeeNode(name)
            print(f"✅ {name} added as the team lead.")

        elif choice == "2":
            manager = input("Enter the manager's name: ").strip()
            employee = input("Enter the new employee's name: ").strip()
            side = input("Should this employee be on the LEFT or RIGHT of the manager? ")
            tree.insert(manager, employee, side)

        elif choice == "3":
            print("\n🌳 Current Team Structure:")
            tree.print_tree()

        elif choice == "4":
            print("Good Bye!")
            break

        else:
            print("❌ Invalid option. Please choose 1–4.")


if __name__ == "__main__":
    company_directory()


"""
DESIGN MEMO

Recursive insertion works by treating every employee as the root of their own
smaller tree. The insert() method starts at the team lead and asks one question:
"Is this the manager I'm looking for?" If yes, it checks whether the requested
side (left or right) is empty and, if so, creates a new EmployeeNode there. If
not, the method calls itself on the left child and then the right child, passing
the same manager name down. Each call handles one node, and the recursion keeps
going until the manager is found or every branch has been checked. The method
returns True or False so the caller knows whether the search succeeded.

The main challenge was handling the default parameter current_node=None. The
instructions say to reset to the root when current_node is None, but an empty
child is also None, so naively recursing into an empty child would jump back to
the root and loop forever. I solved this by only recursing into children that
exist and by remembering whether the current call is the top-level one. That
also fixed a second problem: without it, the "manager not found" error printed
once for every dead end instead of once overall. Validating the side input
("left" vs "right") and reporting who already occupies a taken spot made the
error messages more useful.

Trees are preferable to flat structures like lists or dictionaries whenever the
data is naturally hierarchical: org charts, file systems, the HTML DOM, menus,
or category structures in an online store. A tree captures parent-child
relationships directly, so questions like "who reports to whom" or "what is
inside this folder" are answered by following links instead of scanning
everything. Ordered variants such as binary search trees also allow fast
searching, inserting, and deleting compared to scanning a list.
"""