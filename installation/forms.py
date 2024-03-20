from django import forms


class SearchRequestForm(forms.Form):
    search_field = forms.CharField(required=True,label="")

    def clean_search_field(self):
        search_field = self.cleaned_data['search_field']
        if len(search_field) < 2:
            message = "لطفا کد درخواست را به درستی وارد کنید"
            raise forms.ValidationError(message)
        return search_field
