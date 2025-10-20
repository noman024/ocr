import time
from typing import Dict, Tuple
from collections import defaultdict, deque
import threading


class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
        self.lock = threading.Lock()
    
    def is_allowed(self, client_ip: str) -> Tuple[bool, int]:
        """Check if request is allowed and return remaining requests"""
        with self.lock:
            now = time.time()
            client_requests = self.requests[client_ip]
            
            # Remove old requests outside the window
            while client_requests and client_requests[0] <= now - self.window_seconds:
                client_requests.popleft()
            
            # Check if under limit
            if len(client_requests) < self.max_requests:
                client_requests.append(now)
                remaining = self.max_requests - len(client_requests)
                return True, remaining
            else:
                remaining = 0
                return False, remaining
    
    def get_remaining(self, client_ip: str) -> int:
        """Get remaining requests for client"""
        with self.lock:
            now = time.time()
            client_requests = self.requests[client_ip]
            
            # Remove old requests
            while client_requests and client_requests[0] <= now - self.window_seconds:
                client_requests.popleft()
            
            return max(0, self.max_requests - len(client_requests))


# Global rate limiter instance
rate_limiter = RateLimiter()
