from datetime import datetime, timedelta

from rest_framework import serializers

from .models import Employee, EmployeeAttendance, EmployeeLeave


class EmployeeSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "user_id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "total_cl",
            "total_sl",
            "total_el",
            "department",
            "designation",
        ]


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "phone",
        ]


class SimpleEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name"]


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    employee = SimpleEmployeeSerializer()

    class Meta:
        model = EmployeeAttendance
        fields = [
            "id",
            "employee",
            "attendance",
            "location",
            "in_time",
            "out_time",
            "duration",
        ]

    duration = serializers.SerializerMethodField(method_name="get_duration")

    def get_duration(self, attendance: EmployeeAttendance):
        # use try - catch for handling exception and timedelta to calculate duration instead of below logic
        if attendance.in_time is not None and attendance.out_time is not None:
            in_time = datetime.time(attendance.in_time)
            out_time = datetime.time(attendance.out_time)
            return f"{out_time.hour - in_time.hour}:{out_time.minute - in_time.minute}:{out_time.second - in_time.second}"
        return "Please fill IN time and OUT time to get total work hours"


class CreateEmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        read_only_fields = ["employee_id"]
        fields = [
            "attendance",
            "location",
            "in_time",
            "out_time",
        ]

    def create(self, validated_data):
        employee_id = self.context["employee_id"]
        print(f"{employee_id} ID")
        return EmployeeAttendance.objects.create(
            employee_id=employee_id, **validated_data
        )


class UpdateEmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = [
            "attendance",
            "location",
            "in_time",
            "out_time",
        ]


class EmployeeLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeave
        fields = [
            "id",
            "employee_id",
            "leave",
            "leave_reason",
            "leave_from",
            "leave_to",
            "total_days",
        ]


# class CreateEmployeeLeaveSerializer(serializers.ModelSerializer):
#     read_only_fields = ["employee_id"]

#     class Meta:
#         model = EmployeeLeave
#         fields = [
#             "id",
#             "leave",
#             "leave_reason",
#             "leave_from",
#             "leave_to",
#             "total_days",
#         ]

#     def create(self, validated_data):
#         employee_id = self.context["employee_id"]
#         employee = Employee.objects.get(id=employee_id)
#         if (
#             validated_data["leave"] == "CL"
#             and employee.total_cl > 0
#             and validated_data["total_days"] < employee.total_cl
#         ):
#             employee.total_cl -= validated_data["total_days"]
#             employee.save()
#         else:
#             raise serializers.ValidationError(
#                 f"You have {employee.total_cl} CL left and you applied for {validated_data['total_days']} CL Please apply for a different leave type."
#             )
#         return EmployeeLeave.objects.create(employee_id=employee_id, **validated_data)


class CreateEmployeeLeaveSerializer(serializers.ModelSerializer):
    read_only_fields = ["employee_id"]

    class Meta:
        model = EmployeeLeave
        fields = [
            "id",
            "leave",
            "leave_reason",
            "leave_from",
            "leave_to",
            "total_days",
        ]

    def create(self, validated_data):
        leave_types = {"CL": "total_cl", "SL": "total_sl", "EL": "total_el"}
        employee_id = self.context["employee_id"]
        employee = Employee.objects.get(id=employee_id)

        leave_type = validated_data["leave"]

        field = leave_types[leave_type]

        balance = getattr(employee, field)

        if balance > 0 and 0 < validated_data["total_days"] <= balance:
            setattr(employee, field, balance - validated_data["total_days"])
            employee.save()
        else:
            raise serializers.ValidationError(
                f"You have {balance} {leave_type} left and you applied for {validated_data['total_days']} {leave_type}. Please apply for a different leave type or a valid number of days."
            )
        return EmployeeLeave.objects.create(employee_id=employee_id, **validated_data)
