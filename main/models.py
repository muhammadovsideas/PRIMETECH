from django.db import models
from django.conf import settings
from users.models import User



# ------------------ MonthlyStats ------------------
class MonthlyStats(models.Model):
    year = models.PositiveIntegerField("Year")
    month = models.PositiveIntegerField("Month")
    total_sales = models.FloatField("Total sales", default=0)
    total_purchases = models.FloatField("Total purchases", default=0)
    total_salaries = models.FloatField("Total salaries", default=0)
    net_profit = models.FloatField("Net profit", default=0)
    expenses = models.FloatField("Expenses", default=0)

    class Meta:
        unique_together = ('year', 'month')
        verbose_name = "Monthly statistics"
        verbose_name_plural = "Monthly statistics"

    def __str__(self):
        return f"{self.year}-{self.month} | Sales: {self.total_sales} | Purchases: {self.total_purchases} | Salaries: {self.total_salaries} | Profit: {self.net_profit} | Expenses: {self.expenses}"


# ------------------ Salary ------------------
class Salary(models.Model):
    gave_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="salaries_given",
        limit_choices_to={"role": User.Role.MANAGER},
        verbose_name="Given by"
    )
    taken_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="salaries_taken",
        limit_choices_to={"role": User.Role.ADMIN},
        verbose_name="Taken by"
    )
    salary_price = models.FloatField("Salary price")
    for_month = models.ForeignKey(MonthlyStats, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Salary"
        verbose_name_plural = "Salaries"


# ------------------ Customer ------------------
class Customer(models.Model):
    name = models.CharField("Name", max_length=255)
    phone_number = models.CharField("Phone number", max_length=13, null=True, blank=True)
    description = models.TextField("Description", null=True, blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": User.Role.ADMIN},
        verbose_name="Created by"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


# ------------------ Category ------------------
class Category(models.Model):
    title = models.CharField("Title", max_length=120)
    description = models.TextField("Description", blank=True, null=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# ------------------ Product ------------------
class Product(models.Model):
    title = models.CharField("Title", max_length=120)
    description = models.TextField("Description", blank=True, null=True)
    brand = models.CharField("Brand", max_length=120)
    price = models.FloatField("Price")
    discount_percentage = models.FloatField("Discount percentage", null=True, blank=True)
    discount_price = models.FloatField("Discount price", null=True, blank=True, editable=False)
    image = models.ImageField("Image", upload_to='products/', blank=True, null=True)
    amount = models.FloatField("Amount", default=1)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,blank=True, verbose_name="Category", related_name="products")

    def save(self, *args, **kwargs):
        if self.discount_percentage is not None:
            self.discount_price = round(self.price - (self.price * self.discount_percentage / 100), 2)
        else:
            self.discount_price = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


# ------------------ Sale ------------------
class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name="Customer")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Product")
    description = models.TextField("Description", blank=True, null=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    quantity = models.PositiveIntegerField("Quantity")
    total_price = models.FloatField("Total price", editable=False)
    sale_date = models.DateTimeField("Sale date", auto_now_add=True)
    sold_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": User.Role.ADMIN},
        verbose_name="Sold by"
    )

    def save(self, *args, **kwargs):
        price_to_use = self.product.discount_price or self.product.price
        self.total_price = round(price_to_use * self.quantity, 2)

        if self.pk is None:  # yangi sotuv
            if self.product.amount < self.quantity:
                raise ValueError("Not enough product in stock!")
            self.product.amount -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale #{self.id} - {self.product.title if self.product else 'Deleted product'}"

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"


# ------------------ Purchase ------------------
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField("Quantity")
    purchase_price = models.FloatField("Purchase price")
    total_cost = models.FloatField("Total cost", editable=False)
    purchase_date = models.DateTimeField("Purchase date", auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_cost = round(self.purchase_price * self.quantity, 2)

        if self.pk is None:  # yangi purchase bo‘lsa
            self.product.amount += self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase of {self.product.title} - {self.total_cost}"

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"


# ------------------ Expense ------------------
class Expense(models.Model):
    description = models.TextField("Description", blank=True, null=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    price = models.FloatField("Price")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Created by"
    )

    def __str__(self):
        return self.description or "Expense"

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

class Images(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField("Image", upload_to='products_images/', blank=True, null=True)

    def __str__(self):
        return f"Image of {self.product.title}"