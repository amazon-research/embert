from transformers import BertConfig

ROI_FEATURES_DIM = 1024
ROI_ANGLES_DIM = 3
ROI_COORDINATES_DIM = 4
ROI_REL_AREA_DIM = 1
VISUAL_EMB_SIZE = ROI_FEATURES_DIM + ROI_ANGLES_DIM + ROI_COORDINATES_DIM + ROI_REL_AREA_DIM
ALFRED_ACTION_SPACE = 13
OSCAR_IMG_FEATURE_DIM = 2054
INFERENCE_TRAJ_LIMIT = 200
NUM_OBJECT_LABELS = 119
# position [0] is the front view and the other are following views going right
NUM_OBJECTS_PER_VIEW = (9, 9, 9, 9)


class EmbodiedBertConfig(BertConfig):
    model_type = "bert"

    def __init__(self,
                 num_objects_per_view=NUM_OBJECTS_PER_VIEW,
                 visual_pos_size=ROI_ANGLES_DIM,
                 visual_emb_size=VISUAL_EMB_SIZE,
                 use_lm_loss=False,
                 use_vm_loss=False,
                 use_itm_loss=False,
                 state_repr_method="hidden",
                 **kwargs):
        """

        :param num_visual_features: maximum number of visual elements that the model receives in input
        :param visual_emb_size: Total size of the visual input tokens
        :param use_lm_loss: Whether to use Vision-Language Masked Modelling loss
        :param use_vm_loss: Whether to use Vision-Language Matching loss
        :param use_pm_loss: Whether to use progress monitor loss
        :param state_repr_method: How to use the hidden state generated by the Transformer to represent the state
        :param kwargs: Same as BERT -- See BertConfig constructor
        """
        super(EmbodiedBertConfig, self).__init__(**kwargs)
        self.num_objects_per_view = num_objects_per_view
        self.num_visual_features = sum(num_objects_per_view)
        self.num_objects_in_front = num_objects_per_view[0]
        self.visual_emb_size = visual_emb_size
        self.visual_pos_size = visual_pos_size
        self.use_lm_loss = use_lm_loss
        self.use_vm_loss = use_vm_loss
        self.use_itm_loss = use_itm_loss
        self.state_repr_method = state_repr_method
        self.oscar_img_feature_dim = OSCAR_IMG_FEATURE_DIM
        self.num_object_labels = NUM_OBJECT_LABELS


class AlfredConfig(EmbodiedBertConfig):
    model_type = "bert"

    def __init__(self, action_loss_weight=1.0, obj_interact_weight=1.0,
                 num_actions=ALFRED_ACTION_SPACE, num_objects_per_view=NUM_OBJECTS_PER_VIEW,
                 visual_pos_size=ROI_ANGLES_DIM,
                 visual_emb_size=VISUAL_EMB_SIZE,
                 use_lm_loss=False, use_vm_loss=False, use_itm_loss=False, use_pm_loss=False,
                 use_start_instr_loss=False,
                 state_repr_method="hidden",
                 use_nav_receptacle_loss=False,
                 **kwargs):
        super().__init__(num_objects_per_view,
                         visual_pos_size, visual_emb_size, use_lm_loss, use_vm_loss,
                         use_itm_loss, state_repr_method, **kwargs)

        self.num_actions = num_actions
        self.action_loss_weight = action_loss_weight
        self.obj_interact_weight = obj_interact_weight
        self.use_pm_loss = use_pm_loss
        self.use_start_instr_loss = use_start_instr_loss
        self.use_nav_receptacle_loss = use_nav_receptacle_loss
