# Version1 experiments

## Average results from version1. Single and Multi-node deployment, 3 replicas for facedetector-faceanalyzer-mobilenet (no pressure)

* Url1's duration = 180 seconds (0-180) with total 11  frames created & processed (1 per 15 seconds)
* Url4's duration = 280 seconds (0-280) with total 18  frames created & processed (1 per 15 seconds)
* Url5's duration = 500 seconds (0-500) with total 26  frames created & processed (1 per 15 seconds)
* Url6's duration = 500 seconds (0-500) with total 78  frames created & processed (1 per 5 seconds)
* Url7's duration = 654 seconds (0-654) with total 130 frames created & processed (1 per 5 seconds)

![single_multi2](https://user-images.githubusercontent.com/57920951/152982651-d522ac39-8d8e-4c61-9a32-cc74b095681b.png)

## Timestamps experiment for Version1(3 replicas) single-node VS Version1(3 replicas) multi-node deployments

![timestamps_with_vals](https://user-images.githubusercontent.com/57920951/154118396-c824ea70-510a-480f-9fe1-18d325f87b14.png)


![timestamps_experiment](https://user-images.githubusercontent.com/57920951/153643250-ea74508f-3049-48b1-a51d-addd0be4791f.png)

## Average results for Version1(1, 3 replicas) for single-node deployment: Davinci VS Liono
*This was done to check whether some of the machines are stronger than others*

![Screenshot from 2022-02-14 12-41-20](https://user-images.githubusercontent.com/57920951/153849266-85194275-68a4-4ccd-bfb9-923df6a0fb2b.png)

## Heatmaps for facedetector part with scaling replica pods and queue-workers

![facedetector_heatmap_7frames_nopressure](https://user-images.githubusercontent.com/57920951/156896587-c3f38b0a-b0c8-4958-a488-267233651aad.png)

![facedetector_heatmap_16frames_nopressure](https://user-images.githubusercontent.com/57920951/156896591-e422d996-cf31-4239-b24f-44df23764bea.png)

![facedetector_heatmap_32frames_nopressure](https://user-images.githubusercontent.com/57920951/156896598-4689bd5c-9070-4f35-b6bf-7cdf1fbc97c5.png)

![facedetector_heatmap_65frames_nopressure](https://user-images.githubusercontent.com/57920951/156896600-33b4b389-a112-4bbc-a0e2-2cd54279559e.png)

## Heatmaps for faceanalyzer-mobilenet part with scaling replica pods and queue-workers

![facemob_heatmap_7frames_nopressure](https://user-images.githubusercontent.com/57920951/156896635-a529c789-633a-4639-a32f-f2cf4bc42406.png)

![facemob_heatmap_16frames_nopressure](https://user-images.githubusercontent.com/57920951/156896640-9d9b3e54-add0-4c59-a82c-15368bb6e123.png)

![facemob_heatmap_32frames_nopressure](https://user-images.githubusercontent.com/57920951/156896644-27725733-674e-484d-b8ae-12229291d5bc.png)

![facemob_heatmap_65frames_nopressure](https://user-images.githubusercontent.com/57920951/156896646-bf420f94-1e01-43a7-b02c-d97abf7e5500.png)

## Heatmaps for pressure applied on facedetector part, with scaling queue-workers

![facedetector_7frames_pressure](https://user-images.githubusercontent.com/57920951/156930870-7673cedf-4951-4fbd-a75d-a000c6c5ec40.png)

![facedetector_16frames_pressure](https://user-images.githubusercontent.com/57920951/156930875-3b4681e0-9154-4c47-ba9d-006562d4482e.png)

![facedetector_32frames_pressure](https://user-images.githubusercontent.com/57920951/156930881-7589b5f5-b10e-4c6c-962c-f75a78a5e88d.png)

![facedetector_65frames_pressure](https://user-images.githubusercontent.com/57920951/156930882-c1c2476e-2600-4e4a-8fc8-716c782ee4c0.png)


