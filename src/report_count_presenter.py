from typing import List
from functools import reduce

from src.abstract_report_count_presenter import AbstractReportCountPresenter
from src.count_entity import CountEntity
from src.report_count_output_data import ReportCountOutputData


class ReportCountPresenter(AbstractReportCountPresenter):
    @classmethod
    def _accumulate(cls, counts: List[CountEntity]):
        return reduce(lambda a, b: a + b.value, counts, 0)

    def complete(self, output: ReportCountOutputData):
        dict = {one_old.key: [one_old.value, 0] for one_old in output.one_old}
        for latest in output.latest:
            if latest.key in dict:
                dict[latest.key][1] = latest.value
            else:
                dict[latest.key] = (0, latest.value)
        for key, value in dict.items():
            print(f'{value[1]:#5} ({value[1]-value[0]:+#5}) {key}')

        one_old_total = ReportCountPresenter._accumulate(output.one_old)
        latest_total = ReportCountPresenter._accumulate(output.latest)
        diff = latest_total - one_old_total
        print(f'{latest_total:#5} ({diff:+#5}) total')


AbstractReportCountPresenter.register(ReportCountPresenter)
