from django.http.response import Http404
from rest_framework import mixins, status, generics
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from Core.models import Student
from Core.models import LateEntry
from django.utils import timezone
import datetime
# ---------Serializers--------
from Core.serializers import LateEntrySerializer, StudentRecordSerializer

def check_date(date):
    n = timezone.now()
    # specific_date
    new_datetime = datetime.datetime(date[0], date[1], date[2], n.hour, n.minute, n.second, n.microsecond, n.tzinfo)
    # specific date should be earlier to today as entries at a future date can't be marked
    if n >= new_datetime:
        # print('entered date is past')
        return new_datetime
    else:
        return False
        # return Response({'message':'Future date entries can\'t be marked'}, status=status.HTTP_400_BAD_REQUEST)

class Scan(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data

        try:
            std = Student.objects.get(st_no=data['st_no'])
            LateEntry.objects.create(student=std)
            return Response({'message':'Late entry registered entered'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'message':'Student data doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)


# specific date entry allowed in manual entry only
class ManualEntry(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        st_no_list = data['st_no_list']

        success = 0

        for i in st_no_list:
            try:
                std = Student.objects.get(st_no=i)
                if not 'date' in data:
                    print("date not provided")
                    LateEntry.objects.create(student=std)
                else:
                    print("date provided")
                    specific_date=check_date(data['date'])
                    if specific_date:
                        LateEntry.objects.create(student=std, created_at=specific_date)
                    else:
                        return Response({'message':'Future date entries can\'t be marked'}, status=status.HTTP_400_BAD_REQUEST)

                success += 1
            except:
                pass

        return Response({'message':f'{success} Late entry registered {len(st_no_list) - success} failed.'}, status=status.HTTP_201_CREATED)

class Record(APIView):
    def get(self, request, format=None):
        std = Student.objects.all()
        serializer = StudentRecordSerializer(std, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
