from django.db import models

from django.db import models
from django.urls import reverse
from django.utils import timezone


def one_week_hence():
    """Returns a date one week from now"""

    return timezone.now() + timezone.timedelta(days=7)


class ToDoList(models.Model):
    """Defines what a ToDoList contains
    
    Attributes:
        title: the name of the list
    Methods:
        get_absolute_url: returns an absolute url
        __str__: returns the name of the ToDo List
    """

    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        """Returns the ToDo List url"""

        return reverse("list", args=[self.id])
    
    def __str__(self):
        """Returns the title of the ToDo List"""

        return self.title
    
class ToDoItem(models.Model):
    """Defines a single ToDo List Item
    
    Atrributes:
        title: of the ToDo list items
        description: of the item
        created_date: when was it created
        due_date: when the item is due
        todo_list: which ToDo List the item belongs to.
    Methods:
    """

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Returns The items url"""

        return reverse(
            "item-update",
            args=[str(self.todo_list.id), str(self.id)],
        )
    
    def __str__(self):
        """Returns info on the item(name and due date)"""

        return f"{self.title}: due {self.due_date}"
    
    class Meta:
        ordering = ["due_date"]