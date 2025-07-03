# src/notifications/services.py

class NotificationService:
    def send_reservation_confirmation(self, email: str, date: str, restaurant_name: str):
        message = f"Notification to {email}: Reservation confirmed for {date} at {restaurant_name}."
        print(message)

    def send_reservation_cancellation(self, email: str, reservation_id: str):
        message = f"Notification to {email}: Reservation (ID: {reservation_id}) has been cancelled."
        print(message)

    def send_preorder_notification(self, email: str, num_dishes: int):
        message = f"Notification to {email}: Pre-order with {num_dishes} dishes registered for your reservation."
        print(message)

# Instancia Singleton para ser usada en la inyección de dependencias
notification_service = NotificationService()