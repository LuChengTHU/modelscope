# Copyright (c) Alibaba, Inc. and its affiliates.

from typing import Dict, Union

from modelscope.metainfo import Pipelines
from modelscope.models import Model
from modelscope.models.nlp import SpaceForDialogModeling
from modelscope.outputs import OutputKeys
from modelscope.pipelines.base import Pipeline, Tensor
from modelscope.pipelines.builder import PIPELINES
from modelscope.preprocessors import DialogModelingPreprocessor
from modelscope.utils.constant import Tasks

__all__ = ['DialogModelingPipeline']


@PIPELINES.register_module(
    Tasks.task_oriented_conversation, module_name=Pipelines.dialog_modeling)
class DialogModelingPipeline(Pipeline):

    def __init__(self,
                 model: Union[SpaceForDialogModeling, str],
                 preprocessor: DialogModelingPreprocessor = None,
                 **kwargs):
        """Use `model` and `preprocessor` to create a dialog modeling pipeline for dialog response generation

        Args:
            model (str or SpaceForDialogModeling): Supply either a local model dir or a model id from the model hub,
            or a SpaceForDialogModeling instance.
            preprocessor (DialogModelingPreprocessor): An optional preprocessor instance.
        """
        model = model if isinstance(
            model, SpaceForDialogModeling) else Model.from_pretrained(model)
        self.model = model
        if preprocessor is None:
            preprocessor = DialogModelingPreprocessor(model.model_dir)
        super().__init__(model=model, preprocessor=preprocessor, **kwargs)
        self.preprocessor = preprocessor

    def postprocess(self, inputs: Dict[str, Tensor]) -> Dict[str, str]:
        """process the prediction results

        Args:
            inputs (Dict[str, Any]): _description_

        Returns:
            Dict[str, str]: the prediction results
        """
        sys_rsp = self.preprocessor.text_field.tokenizer.convert_ids_to_tokens(
            inputs['resp'])
        assert len(sys_rsp) > 2
        sys_rsp = sys_rsp[1:len(sys_rsp) - 1]
        inputs[OutputKeys.OUTPUT] = sys_rsp

        return inputs
