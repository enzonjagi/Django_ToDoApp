from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import ToDoItem, ToDoList
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.
class ListListView(ListView):
    """Defines the ToDo List's view
    
    Attributes:
        model: the data-model class to be fetched
        template_name: the template we'll be formatting the list
            into a view
    """

    model = ToDoList
    template_name = "todo_app/index.html"

class ItemListView(ListView):
    """Defines the ToDo List Item's View
    
    Attributes:
        model: the todoItem model class to be fetched
        template_name: where we'll format the model's content
            into a view
    Methods:
        get_query_set: 
        get_context_data:
    """

    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        """
        Restricts the data returned 
        to display only the list's to do items
        """

        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])
    
    def get_context_data(self):
        """
        Ensures the Todo object is also returned, not just the items

        Also merges the existing data by calling the OG .get_contex_data() 
        """

        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context
    
class ListCreate(CreateView):
    """Allows user to create a List view
    
    This class defines a form containing the sole public ToDoList attribute, 
    its title.
    The form itself also has a title, which is passed in the context data.
    """

    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context
    
class ItemCreate(CreateView):
    """Allows user to create a List Item view
    
    This generates a form with four fields. 
    The .get_initial() and .get_context_data() methods are overridden 
    to provide useful information to the template. 
    The .get_success_url() method provides the view with a page to display 
    after the new item has been created. 
    """


    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])
    
class ItemUpdate(UpdateView):
    """Allows user to update an item"""

    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])
    
class ListDelete(DeleteView):
    """Allows a user to Delete a List"""

    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    """Allows a user to delete a list item"""

    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context