import asyncio
from typing import Callable, List, Tuple

class RungeKuttaMethod:
    def __init__(self, x_start: float, y_start: float, x_end: float, step_size: float, differential_equation: Callable[[float, float], float]):
        self._differential_equation = differential_equation
        self._step_size = step_size
        self._x_end = x_end
        self._x_start = x_start
        self._y_start = y_start
        self._state = asyncio.Queue()

        asyncio.create_task(self.runge_kutta_full())

    @property
    def differential_equation(self):
        return self._differential_equation

    @differential_equation.setter
    def differential_equation(self, value):
        self._differential_equation = value
        asyncio.create_task(self.runge_kutta_full())

    @property
    def step_size(self):
        return self._step_size

    @step_size.setter
    def step_size(self, value):
        self._step_size = value
        asyncio.create_task(self.runge_kutta_full())

    @property
    def x_end(self):
        return self._x_end

    @x_end.setter
    def x_end(self, value):
        self._x_end = value
        asyncio.create_task(self.runge_kutta_full())

    @property
    def x_start(self):
        return self._x_start

    @x_start.setter
    def x_start(self, value):
        self._x_start = value
        asyncio.create_task(self.runge_kutta_full())

    @property
    def y_start(self):
        return self._y_start

    @y_start.setter
    def y_start(self, value):
        self._y_start = value
        asyncio.create_task(self.runge_kutta_full())

    async def get_state(self) -> List[Tuple[float, float]]:
        return await self._state.get()

    def runge_kutta_step(self, x_current: float, step_size: float, y_current: float, differential_equation: Callable[[float, float], float]) -> float:
        assert step_size > 0, "stepSize should be greater than zero"
        first_bruh = differential_equation(x_current, y_current)
        second_bruh = differential_equation(x_current + step_size / 2, y_current + (step_size * first_bruh) / 2.0)
        third_bruh = differential_equation(x_current + step_size / 2, y_current + (step_size * second_bruh) / 2.0)
        fourth_bruh = differential_equation(x_current + step_size, y_current + (step_size * third_bruh))
        delta = (step_size / 6.0) * (first_bruh + 2.0 * second_bruh + 2.0 * third_bruh + fourth_bruh)

        return y_current + delta

    async def runge_kutta_full(self):
        assert self._x_start < self._x_end, "xEnd should be greater than xStart"
        assert self._step_size > 0, "stepSize should be greater than zero"

        points = [(self._x_start, self._y_start)]
        y_current = self._y_start
        x_current = self._x_start

        while x_current < self._x_end:
            y_current = self.runge_kutta_step(x_current, self._step_size, y_current, self._differential_equation)
            x_current += self._step_size
            points.append((x_current, y_current))

        await self._state.put(points)

    def close(self):
        self._state = asyncio.Queue()


