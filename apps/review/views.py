from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.request import Request
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


from .serializers import CommentCRUDSerializer
from .models import Comment
from .permissions import IsOwner
from apps.hotel.models import Hotel

# class CommentView(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.ListModelMixin,
#     GenericAPIView):

#     permission_classes=
    
#     queryset = Comment.objects.all()
#     serializer_class = CommentCRUDSerializer

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context

class CreateComment(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentCRUDSerializer
    # permission_classes = [IsAuthenticated]
    
    def create(self, request, slug, pk=None):
        hoti = str(request).split('add_comment/')[1].replace("/'>", '')
        print(hoti)
        hotel = Hotel.objects.get(slug=slug)
        serializer = CommentCRUDSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user, hotel=hotel)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                    )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class DesUpdComment(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCRUDSerializer

    permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser, IsOwner]

    def destroy(self, request, slug, pk):
        try:
            obj = Comment.objects.get(pk=pk)
            obj_ = Hotel.objects.get(slug=slug)
            return Response('Комментарий успешно удален')
        except Comment.DoesNotExist:
            return Response('Страница не найдена!', status=status.HTTP_404_NOT_FOUND)

    def update(self, request, slug, pk):
        try:
            obj = Comment.objects.get(pk=pk)
            obj_ = Hotel.objects.get(slug=slug)
            serailizer = CommentCRUDSerializer(data=request.data)
            if serailizer.is_valid(raise_exception=True):
                serailizer.save()

                
            return Response('Комментарий успешно изменен')
        except Comment.DoesNotExist:
            return Response('Страница не найдена!', status=status.HTTP_404_NOT_FOUND)

        

    




# from rest_framework.views import APIView

# from .serializers import CommentCRUDSerializer
# from .models import Comment
# from .permissions import IsOwner


# class CommentApiView(APIView):

#     permission_classes=[IsAuthenticated]
    
#     def create_comment(self, request: Request, pk=None):
#         hotel = self.get_object()
#         serializer = CommentCRUDSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid(raise_exception=True):
#             if request.method == 'POST':
#                 serializer.save(user=request.user, hotel=hotel)
#                 return Response(
#                     serializer.data, status=status.HTTP_201_CREATED
#                     )

#     def get_comment(self, request: Request):
#         comments = Comment.objects.all()
#         serialiser = CommentCRUDSerializer(comments, many=True)

#         return Response(
#             data={
#                 'message': 'hello',
#                 'data': [1,2,3],
#                 'comments': serialiser.data
#                 }
#                 )
#     permission_classes=[IsOwner]

#     def delete(self, request, slug, pk):
#         try:
#             obj = Comment.objects.get(pk=pk).delete()
#             obj_ = Hotel.objects.get(slug=slug)
#             return Response('Комментарий успешно удален')
#         except Comment.DoesNotExist:
#             return Response('Страница не найдена!', status=status.HTTP_404_NOT_FOUND)

#     def update(self, request, slug, pk):
#         try:
#             obj = Comment.objects.get(pk=pk).patch()
#             obj_ = Hotel.objects.get(slug=slug)
#             return Response('Комментарий успешно изменен')
#         except Comment.DoesNotExist:
#             return Response('Страница не найдена!', status=status.HTTP_404_NOT_FOUND)


# class BookApiView(APIView):

#     def get(self, request: Request):
#         # print(request.data)
#         books = Book.objects.all()
#         serialiser = BookSerializer(books, many=True)

#         return Response(
#             data={
#                 'message': 'hello',
#                 'data': [1,2,3],
#                 'books': serialiser.data
#                 }
#                 )

    

#     def get_object(self, pk):
#         try:
#             return Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             raise Http404

#     def put(self, request, pk):
#         book = self.get_object(pk)
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)