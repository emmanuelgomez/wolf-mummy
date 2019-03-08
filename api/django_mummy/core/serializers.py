from rest_framework import serializers
from .models import Investor, Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = '__all__'

# class MummyInvestorsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Investor
#         fields = ('innocence', 'experience','charisma','money' )

# class MummySerializer(serializers.ModelSerializer):
#     parent = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     # mummyInvestors = serializers.MummyInvestorsSerializer()
#
#     class Meta:
#         model = Investor
#         fields = ('parent', 'innocence', 'experience','charisma','money')


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class MummySerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Investor
        fields = ('id',  'innocence', 'experience','charisma','money', 'parent', 'children')