model = dict(
    type='Recognizer3D',
    backbone=dict(
        type='ResNet3dSlowOnly',
        in_channels=5,
        base_channels=32,
        num_stages=3,
        out_indices=(2, ),
        stage_blocks=(4, 6, 3),
        conv1_stride=(1, 1),
        pool1_stride=(1, 1),
        inflate=(0, 1, 1),
        spatial_strides=(2, 2, 2),
        temporal_strides=(1, 1, 2)),
    cls_head=dict(
        type='I3DHead', in_channels=512, num_classes=10, dropout=0.5),
    test_cfg=dict(average_clips='prob'))
dataset_type = 'PoseDataset'
ann_file = 'data/ds_taichi/test9nsnr.pkl'
left_kp = [
    5, 6, 7, 8, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
    60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71
]
right_kp = [
    1, 2, 3, 4, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43
]
train_pipeline = [
    dict(type='UniformSampleFrames', clip_len=48),
    dict(type='PoseDecode'),
    dict(type='PoseCompact', hw_ratio=1.0, allow_imgpad=True),
    dict(type='Resize', scale=(-1, 64)),
    dict(type='RandomResizedCrop', area_range=(0.56, 1.0)),
    dict(type='Resize', scale=(56, 56), keep_ratio=False),
    dict(
        type='Flip',
        flip_ratio=0.5,
        left_kp=[
            5, 6, 7, 8, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
            58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71
        ],
        right_kp=[
            1, 2, 3, 4, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43
        ]),
    dict(type='GenerateTaiChiPoseTarget', with_kp=True, with_limb=False),
    dict(type='FormatShape', input_format='NCTHW_Heatmap'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
val_pipeline = [
    dict(type='UniformSampleFrames', clip_len=48, num_clips=1),
    dict(type='PoseDecode'),
    dict(type='PoseCompact', hw_ratio=1.0, allow_imgpad=True),
    dict(type='Resize', scale=(64, 64), keep_ratio=False),
    dict(type='GenerateTaiChiPoseTarget', with_kp=True, with_limb=False),
    dict(type='FormatShape', input_format='NCTHW_Heatmap'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
test_pipeline = [
    dict(type='UniformSampleFrames', clip_len=48, num_clips=10),
    dict(type='PoseDecode'),
    dict(type='PoseCompact', hw_ratio=1.0, allow_imgpad=True),
    dict(type='Resize', scale=(64, 64), keep_ratio=False),
    dict(
        type='GenerateTaiChiPoseTarget',
        with_kp=True,
        with_limb=False,
        double=True),
    dict(type='FormatShape', input_format='NCTHW_Heatmap'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
data = dict(
    videos_per_gpu=8,
    workers_per_gpu=4,
    test_dataloader=dict(videos_per_gpu=6),
    train=dict(
        type='RepeatDataset',
        times=30,
        dataset=dict(
            type='PoseDataset',
            ann_file='data/ds_taichi/test9nsnr.pkl',
            split='train',
            pipeline=[
                dict(type='UniformSampleFrames', clip_len=48),
                dict(type='PoseDecode'),
                dict(type='PoseCompact', hw_ratio=1.0, allow_imgpad=True),
                dict(type='Resize', scale=(-1, 64)),
                dict(type='RandomResizedCrop', area_range=(0.56, 1.0)),
                dict(type='Resize', scale=(56, 56), keep_ratio=False),
                dict(
                    type='Flip',
                    flip_ratio=0.5,
                    left_kp=[
                        5, 6, 7, 8, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                        55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
                        69, 70, 71
                    ],
                    right_kp=[
                        1, 2, 3, 4, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                        27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                        41, 42, 43
                    ]),
                dict(
                    type='GenerateTaiChiPoseTarget',
                    with_kp=True,
                    with_limb=False),
                dict(type='FormatShape', input_format='NCTHW_Heatmap'),
                dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
                dict(type='ToTensor', keys=['imgs', 'label'])
            ])),
    val=dict(
        type='PoseDataset',
        ann_file='data/ds_taichi/test9nsnr.pkl',
        split='test',
        pipeline=[
            dict(type='UniformSampleFrames', clip_len=48, num_clips=1),
            dict(type='PoseDecode'),
            dict(type='PoseCompact', hw_ratio=1.0, allow_imgpad=True),
            dict(type='Resize', scale=(64, 64), keep_ratio=False),
            dict(
                type='GenerateTaiChiPoseTarget', with_kp=True,
                with_limb=False),
            dict(type='FormatShape', input_format='NCTHW_Heatmap'),
            dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
            dict(type='ToTensor', keys=['imgs'])
        ]),
    test=dict(
        type='PoseDataset',
        ann_file='data/ds_taichi/test9nsnr.pkl',
        split='test',
        pipeline=[
            dict(type='UniformSampleFrames', clip_len=48, num_clips=10),
            dict(type='PoseDecode'),
            dict(type='PoseCompact', hw_ratio=1.0, allow_imgpad=True),
            dict(type='Resize', scale=(64, 64), keep_ratio=False),
            dict(
                type='GenerateTaiChiPoseTarget',
                with_kp=True,
                with_limb=False,
                double=True),
            dict(type='FormatShape', input_format='NCTHW_Heatmap'),
            dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
            dict(type='ToTensor', keys=['imgs'])
        ]))
optimizer = dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0003)
optimizer_config = dict(grad_clip=dict(max_norm=40, norm_type=2))
lr_config = dict(policy='CosineAnnealing', by_epoch=False, min_lr=0)
total_epochs = 24
checkpoint_config = dict(interval=24)
evaluation = dict(
    interval=1, metrics=['top_k_accuracy', 'mean_class_accuracy'], topk=(1, 5))
log_config = dict(interval=20, hooks=[dict(type='TextLoggerHook')])
log_level = 'INFO'
output_config = dict(
    out='./model_pth/exp5/t9nsnr_5p_ft_lrd01_nopre/test_result/results.pkl')
eval_config = dict(
    metric_out='./model_pth/exp5/t9nsnr_5p_ft_lrd01_nopre/test_result',
    eval=[
        'top_k_accuracy', 'mean_class_accuracy', 'confusion_matrix',
        't_sne_vis'
    ])
work_dir = './model_pth/exp5/t9nsnr_5p_ft_lrd01_nopre'
load_from = None
find_unused_parameters = True
dist_params = dict(backend='nccl')
gpu_ids = range(0, 4)
