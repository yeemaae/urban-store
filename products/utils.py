# utils.py
from django.db.models import Count, Q
from .models import Product, UserSearchLog


def get_recommended_products(user):
    if user.is_authenticated:
        popular_queries = UserSearchLog.objects.filter(user=user).values('query').annotate(
            count=Count('query')).order_by('-count')[:5]

        # Debugging: Print the queries and check if there are results
        print("Popular Queries:", popular_queries)

        recommendations = Product.objects.none()
        for entry in popular_queries:
            query = entry['query']
            recommendations |= Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        # Debugging: Check if there are any recommended products
        print("Recommendations:", recommendations)
        return recommendations.distinct()

    return Product.objects.none()
