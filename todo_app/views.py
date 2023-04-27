from django.shortcuts import render
from .models import ToDoItem, ToDoList
from django.views.generic import ListView

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