from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from users.permissions import *
from .serializers import *
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="List all categories with search and ordering",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by title or description',
                              type=openapi.TYPE_STRING),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                description='Order by id or title',
                type=openapi.TYPE_STRING,
                enum=['title', '-title']
            ),
        ]
    )
    def get(self, request):
        categories = Category.objects.all()

        search = request.GET.get('search')
        if search:
            categories = categories.filter(title__icontains=search) | categories.filter(description__icontains=search)

        ordering = request.GET.get('ordering')
        if ordering in ['title', '-title']:
            categories = categories.order_by(ordering)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="List all products with search, price filtering and ordering",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by title, description, or brand',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description='Filter by minimum price',
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description='Filter by maximum price',
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('category', openapi.IN_QUERY, description='Filter by category id',
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                description='Order by price, created_at or title',
                type=openapi.TYPE_STRING,
                enum=['price', '-price', 'title', '-title']
            ),
        ]
    )
    def get(self, request):
        products = Product.objects.all()

        search = request.GET.get('search')
        if search:
            products = products.filter(title__icontains=search) | products.filter(
                description__icontains=search) | products.filter(brand__icontains=search)

        min_price = request.GET.get('min_price')
        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                pass

        max_price = request.GET.get('max_price')
        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                pass

        category_id = request.GET.get('category')
        if category_id:
            try:
                products = products.filter(category_id=int(category_id))
            except ValueError:
                pass

        ordering = request.GET.get('ordering')
        if ordering in ['price', '-price', 'title', '-title']:
            products = products.order_by(ordering)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ImageListAPIView(ListAPIView):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = [AllowAny]

class CartListAPIView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class AboutRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AboutSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return About.objects.first()

class AnnouncementListAPIView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [AllowAny]



class AnnouncementRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [AllowAny]








