from arekit.common.experiment.data_type import DataType
from arekit.contrib.experiment_rusentrel.ops_opin import OpinionOperations
from arekit.contrib.experiment_rusentrel.labels.scalers.ruattitudes import ExperimentRuAttitudesLabelConverter
from arekit.contrib.source.ruattitudes.opinions.utils import RuAttitudesSentenceOpinionUtils


class RuAttitudesOpinionOperations(OpinionOperations):

    def __init__(self, ru_attitudes):
        assert(isinstance(ru_attitudes, dict) or ru_attitudes is None)
        super(RuAttitudesOpinionOperations, self).__init__()

        self.__ru_attitudes = ru_attitudes
        self.__label_scaler = ExperimentRuAttitudesLabelConverter()

    # region private methods

    def __get_opinion_list_in_doc(self, doc_id, opinion_check=lambda _: True):
        news = self.__ru_attitudes[doc_id]

        data_it = RuAttitudesSentenceOpinionUtils.iter_opinions_with_related_sentences(
            news=news, label_scaler=self.__label_scaler)

        return [opinion for opinion, _ in data_it if opinion_check(opinion)]

    # endregion

    def iter_opinions_for_extraction(self, doc_id, data_type):

        opinion_lists = []

        if data_type == DataType.Train:
            # We provide only those opinions that
            # were labeled in RuAttitudes collection
            opinion_lists.append(self.__get_opinion_list_in_doc(doc_id=doc_id))

        for collection in opinion_lists:
            for opinion in collection:
                yield opinion

    def get_etalon_opinion_collection(self, doc_id):
        return self.__get_opinion_list_in_doc(doc_id=doc_id)
