from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, QuoteForm
from .models import Author, Quote


def base(request):
    return render(request, 'quotes_app/base.html')


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'quotes_app/author_list.html', {'authors': authors})


def quote_list(request, author_id=None):
    if author_id is not None:
        author = get_object_or_404(Author, pk=author_id)
        quotes = Quote.objects.filter(author=author)
    else:
        quotes = Quote.objects.all()

    return render(request, 'quotes_app/quote_list.html', {'quotes': quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            try:
                author = Author.objects.get(fullname=fullname)
            except Author.DoesNotExist:
                author = Author(fullname=fullname)
                author.save()
                return redirect('quotes_app:author_list')
            except IntegrityError:
                pass
    else:
        form = AuthorForm()
    return render(request, 'quotes_app/add_author.html', {'form': form})


@login_required
def add_quote(request):
    form = QuoteForm()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            author_id = form.cleaned_data['author'].id
            author = get_object_or_404(Author, id=author_id)
            quote.author = author
            quote.save()
            return redirect('quotes_app:quote_list')
    else:
        
        print(form.errors)
        form = QuoteForm()
    return render(request, 'quotes_app/add_q.html', {'form': form})




def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'quotes_app/author_detail.html', {'author': author})


def quote_list_by_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name)
    return render(request, 'quotes_app/quote_list_by_tag.html', {'tag_name': tag_name, 'quotes': quotes})
