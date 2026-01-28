from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Please leave a good/bad review of your esperience please?"
            }),
        }
