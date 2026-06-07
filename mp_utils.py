from multiprocessing import cpu_count, Pool
from typing import Any, Callable, List

from log import log


def _map_reduce_wrapper(kwargs: dict) -> Any:
    func: Callable = kwargs.pop("func")
    return func(**kwargs)


def map_reduce(func: Callable, kwargs_list: List[dict], processes: int = cpu_count(), async_: bool = False) -> List[Any]:
    if processes == 0:
        processes = cpu_count()
    log.info(f"Run function {func.__name__} @ {processes} threads on {len(kwargs_list)} items")
    pool = Pool(processes=processes)
    for kwargs in kwargs_list:
        kwargs["func"] = func
    if async_:
        result = pool.map_async(func=_map_reduce_wrapper, iterable=kwargs_list)
    else:
        result = pool.map(func=_map_reduce_wrapper, iterable=kwargs_list)
    pool.close()
    pool.join()
    if async_:
        return result.get()
    return result
