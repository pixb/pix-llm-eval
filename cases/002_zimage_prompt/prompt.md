---
id: 002_zimage_prompt
name: z-image-turbo prompt generation (cold start)
type: prompt-engineering / text-to-image
canvas: 1920x1080 (16:9)
---

你是文生图提示词工程师。为模型 **z-image-turbo** 写一段提示词，生成下述场景的插画。

## 场景描述

中国传统工笔淡彩插画，横幅 1920×1080：

- 一条古老石阶蜿蜒上山，石面被岁月磨得光滑，边缘覆着青苔
- 石阶两侧翠竹成林，竹叶低垂拂过阶面
- 石阶向上延伸，逐渐消失在山间晨雾中
- 林间有柔和的光束斜落，照亮部分苔阶
- 阶上散落金黄落叶，随风飘舞
- 画面一角有一位年老的僧人，正在清扫落叶；全身入画，身形较小，不喧宾夺主
- 整体色调：翡翠绿为主，淡金点缀；气氛幽静深远

## 要求

1. 只输出一段**纯英文**提示词，不要中文、不要解释、不要 markdown 格式
2. 提示词需适配 z-image-turbo 的生成特性：CFG=1，即**单段纯正向描述**——
   全文禁止任何否定词（`no` / `not` / `without` / `avoid` / `never` /
   `don't` / `excluding` / `nor` / `neither` / `free of` / `devoid of` …）
   以及任何负面提示（negative prompt）语句
3. 结尾附画质后缀，如 `8K ultra-detailed, high resolution`
