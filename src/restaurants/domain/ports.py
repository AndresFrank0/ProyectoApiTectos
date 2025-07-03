# src/restaurants/domain/ports.py
from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from.entities import Restaurant, Table

class IRestaurantRepository(ABC):
    @abstractmethod
    def get_by_id(self, restaurant_id: uuid.UUID) -> Optional:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def save(self, restaurant: Restaurant) -> Restaurant:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, restaurant_id: uuid.UUID) -> None:
        raise NotImplementedError

class ITableRepository(ABC):
    @abstractmethod
    def get_by_id(self, table_id: uuid.UUID) -> Optional:
        raise NotImplementedError

    @abstractmethod
    def get_by_restaurant_and_number(self, restaurant_id: uuid.UUID, table_number: int) -> Optional:
        raise NotImplementedError

    @abstractmethod
    def get_tables_by_restaurant(self, restaurant_id: uuid.UUID) -> List:
        raise NotImplementedError
    
    @abstractmethod
    def save(self, table: Table) -> Table:
        raise NotImplementedError
        
    @abstractmethod
    def delete(self, table_id: uuid.UUID) -> None:
        raise NotImplementedError