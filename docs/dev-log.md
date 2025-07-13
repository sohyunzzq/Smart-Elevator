# ❌ 한계

## 1. 출력 도구 및 용지 설정 문제

- 적절한 출력 도구와 출력 용지를 발견하지 못함.  
- 출력 강도를 높이기 위해 9V 이상의 높은 전압을 인가하자 **솔레노이드의 발열이 심해져** 전압을 일정 이상 늘릴 수 없었음.  
- 동일한 지점에 여러 번 출력하는 방법도 고려했으나, 출력할 때마다 **용지 위치가 미세하게 움직여** 출력이 흐려졌음.  
- 용지를 팽팽하게 고정한 상태에서 출력하면 **출력 도구가 장력을 이기지 못해 출력되지 않음**.

---

## 🧪 출력 실험

### 🔹 다양한 재질에 출력 테스트

| 실험 재질 | 결과 |
|-----------|------|
| 엠보싱 테이프 / 종이 / 비닐 | 출력이 뚜렷하지 않아 식별 불가 |
| 센터포인터 | 무게 때문에 솔레노이드 출력 강도 약화 |
| 점퍼선 | 출력 면적이 너무 작아 인식 불가 |
| 3D 프린터 핀 | 끝이 뭉툭해 선명하지 않음 |

<img width="251" height="186" alt="실험1" src="https://github.com/user-attachments/assets/f9b7217c-e460-4314-9723-fa9ff7c9d23c" />
<img width="251" height="186" alt="실험2" src="https://github.com/user-attachments/assets/21896644-48eb-4978-b04b-fe2836772da0" />
<img width="251" height="186" alt="실험3" src="https://github.com/user-attachments/assets/dc6ee263-afe4-40fe-953b-d7a47503b594" />

<img width="277" height="200" alt="센터포인터" src="https://github.com/user-attachments/assets/324eb8b4-d1f1-437a-86b2-4f26ed7428bd" />
<img width="317" height="200" alt="점퍼선" src="https://github.com/user-attachments/assets/f71d9aa3-06f0-4fb3-9209-c5fc396e88ae" />
<img width="206" height="200" alt="3D핀" src="https://github.com/user-attachments/assets/603c1d86-a8f4-44cc-b4bc-967a102c157b" />

---

## ✅ 결론

- 종이에 점자를 인쇄하는 방법은 **출력 압력, 출력 도구의 정밀도, 출력 재질의 문제로 인해 어려움**이 있음.  
- 최종적으로는 **종이 인쇄 방식 대신, 솔레노이드로 직접 점자를 튀어나오게 하여 손으로 감지하는 방식**으로 목표를 변경함.
