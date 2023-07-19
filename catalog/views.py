from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from catalog.forms import AuthorCreationForm, BookForm, BookSearchForm
from catalog.models import Book, Author, LiteraryFormat


# Create your views here.

@login_required
def index(request, uniq_number: int = 1):
    num_books = Book.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    num_authors = Author.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_literary_formats": num_literary_formats,
        "num_visits": num_visits
    }
    return render(request, "catalog/index.html", context=context)


class LiteraryFormatListView(LoginRequiredMixin, generic.ListView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_list.html"
    context_object_name = "literary_formats_list"


class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_form.html"


class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_form.html"


class LiteraryFormatDeleteView(generic.DeleteView):
    model = LiteraryFormat
    context_object_name = "format_delete"
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_confirm_delete.html"


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = "catalog/book_list.html"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = BookSearchForm()

        return context

    def get_queryset(self):
        queryset = Book.objects.select_related("format")
        title = self.request.GET.get("title")

        if title:
            return queryset.filter(title__icontains=title)
        return queryset


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = "catalog/book_form.html"
    success_url = reverse_lazy("catalog:book-list")


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    success_url = reverse_lazy("catalog:book-list")
    template_name = "catalog/book_form.html"
    form_class = BookForm


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 2
    template_name = "catalog/author_list.html"


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    success_url = reverse_lazy("catalog:author-list")
    form_class = AuthorCreationForm
    template_name = "catalog/author_form.html"

# def book_detail_view(request, pk):
#     book = Book.objects.get(pk=pk)
#     context = {
#         "book": book,
#     }
#
#     return render(request, "catalog/book_detail.html", context=context)

# def literary_formats_list_view(request):
#     literary_formats = LiteraryFormat.objects.all()
#     context = {
#         "literary_formats": literary_formats
#     }
#     return render(request, "catalog/literary_format_list.html", context=context)
