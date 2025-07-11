from django import forms
from ..models.product import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]
            ),
            "comment": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your review..."}
            ),
        }
