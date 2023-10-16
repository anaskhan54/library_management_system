from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from api.models import Book
from api.serializers import BookSerializer

@csrf_exempt
def book_list(request):
    if request.method=='GET':
        #GET request on /books
        books=Book.objects.all()
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)
    if request.method=='POST':
        try:
            data=JSONParser().parse(request)
            serializer=BookSerializer(data=data)
            serializer.is_valid()
            serializer.save()
            return JsonResponse({"message":"Book Added!"},status=201,safe=False)
        except:
           return JsonResponse(serializer.errors,status=400,safe=False)
    if request.method=='DELETE':
        Book.objects.all().delete()
        return JsonResponse({"message":"All Books Deleted!"},status=204,safe=False)
def find_n(request,n):
    try:
        books=Book.objects.filter(inventory__lt=n)
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)
    except:
        return JsonResponse({"message":"No Books Found!"},status=404,safe=False)

def unavailable_books(request):
    try:
        books=Book.objects.filter(inventory=0)
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)
    except:
        return JsonResponse({"message":"No Books Found!"},status=404,safe=False)
@csrf_exempt
def book_adv(request,isbn_no):
    if request.method=='GET':
        try:
            book=Book.objects.filter(isbn_no=isbn_no).first()
            serializer=BookSerializer(book)
            return JsonResponse(serializer.data,safe=False)
        except:
            return JsonResponse({"message":"Book Not Found!"},status=404,safe=False)
    if request.method=='PUT':
        book_to_update=Book.objects.filter(isbn_no=isbn_no).first()
        data=JSONParser().parse(request)
        serializer=BookSerializer(book_to_update,data=data)
        try:
            serializer.is_valid()
            serializer.save()
            return JsonResponse({"message":"Book Replaced!"},status=201,safe=False)
        except:
            return JsonResponse(serializer.errors,status=400,safe=False)
    if request.method=='PATCH':
        book_to_update=Book.objects.filter(isbn_no=isbn_no).first()
        data=JSONParser().parse(request)
        serializer=BookSerializer(book_to_update,data=data,partial=True)
        try:
            serializer.is_valid()
            serializer.save()
            return JsonResponse({"message":"Book Updated!"},status=201,safe=False)
        except:
            return JsonResponse(serializer.errors,status=400,safe=False)
    if request.method=='DELETE':
        book_to_delete=Book.objects.filter(isbn_no=isbn_no).first()
        book_to_delete.delete()
        return JsonResponse({"message":"Book Deleted!"},status=204,safe=False)
@csrf_exempt
def issue_book(request,isbn_no):

    issued_book=Book.objects.filter(isbn_no=isbn_no).first()
    if issued_book.inventory==0:
        return JsonResponse({"message":"Book Not Available!"},status=404,safe=False)
    issued_book.inventory-=1
    issued_book.save()
    return JsonResponse({"message":"Book Issued!"},status=200,safe=False)
    


