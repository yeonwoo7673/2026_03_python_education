import json
import os

## 게임 관리 클래스
class Quiz:
    """개별 퀴즈 정보를 담는 클래스"""
    def __init__(self, question, answer):
        self.question = question # 질문
        self.answer = answer     # 정답

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.file_path = "state.json"
        self.load_state()

    def init_quizzes(self):
        """초기 퀴즈 데이터 생성"""
        initial_data = [
            ("파이썬에서 리스트에 요소를 추가하는 메서드는?", "append"),
            ("파이썬의 창시자 이름은?", "귀도 반 로섬"),
            ("JSON의 약자는 JavaScript Object 무엇일까요?", "Notation"),
            ("파이썬에서 나머지를 구하는 연산자는?", "%"),
            ("객체지향 프로그래밍의 약자는?", "OOP")
        ]
        for question, answer in initial_data:
            self.quizzes.append(Quiz(question, answer)) 
        print(f"{len(self.quizzes)}개의 기본 퀴즈가 준비되었습니다.")

    def load_state(self):
        """파일에서 데이터 불러오기"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quizzes = [Quiz(q['question'], q['answer']) for q in data['quizzes']]
                    self.high_score = data.get('high_score', 0)
                print("데이터를 성공적으로 불러왔습니다.")
            except (json.JSONDecodeError, KeyError):
                print("파일 형식이 잘못되어 초기 데이터를 사용합니다.")
                self.init_quizzes()
        else:
            self.init_quizzes()
            self.save_state()

    # JSON 파일에 현재 상태를 저장하는 메서드
    def save_state(self):
        """현재 상태를 파일에 저장하기"""
        data = {
            "quizzes": [{"question": q.question, "answer": q.answer} for q in self.quizzes],
            "high_score": self.high_score
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # 사용자 정답 체크 로직
    def play_quiz(self):
        """퀴즈를 풀고 점수를 계산하는 메서드"""
        print(f"\n--- 퀴즈 시작! (현재 최고 점수: {self.high_score}) ---")
        score = 0
        for i, q in enumerate(self.quizzes, 1):
            print(f"\n문제 {i}: {q.question}")
            
            user_answer = ""
            while not user_answer:
                user_answer = input("정답 입력: ").strip()
                if not user_answer:
                    print("답변을 입력해야 합니다!")
            
            if user_answer.lower() == q.answer.lower():
                print("정답입니다! ✨")
                score += 1
            else:
                print(f"아쉽네요. 정답은 '{q.answer}'입니다. 😅")
        
        # for문이 완전히 끝난 후 실행되는 블록
        print(f"\n게임 종료! 이번 점수: {score}/{len(self.quizzes)}")

        if score > self.high_score:
            print(f"🎊 축하합니다! 최고 점수가 {self.high_score}에서 {score}로 갱신되었습니다!")
            self.high_score = score
            self.save_state()

    def add_quiz(self):
        """새로운 퀴즈 추가"""
        question = input("새로운 질문을 입력하세요: ").strip()
        answer = input("정답을 입력하세요: ").strip()
        
        if question and answer:
            self.quizzes.append(Quiz(question, answer))
            self.save_state()
            print("새로운 퀴즈가 저장되었습니다!")
        else:
            print("질문과 정답을 모두 입력해야 합니다.")

    def show_all_quizzes(self):
        """등록된 모든 퀴즈 목록 보기"""
        if not self.quizzes:
            print("\n현재 등록된 퀴즈가 없습니다.")
            return
            
        print("\n--- 현재 등록된 퀴즈 목록 ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question} (정답: {q.answer})")

# 메인 실행 로직
if __name__ == "__main__":
    game = QuizGame()
    
    while True:
        print("\n" + "="*20)
        print("[ 퀴즈 게임 메뉴 ]")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 종료")
        print("="*20)
        
        choice = input("원하는 메뉴 번호를 입력하세요: ").strip()
        
        if choice == '1':
            if not game.quizzes:
                print("⚠️ 풀 수 있는 퀴즈가 없습니다.")
            else:
                game.play_quiz()
        elif choice == '2':
            game.add_quiz()
        elif choice == '3':
            game.show_all_quizzes()
        elif choice == '4':
            print("게임을 종료합니다. 안녕히 가세요!")
            break
        else:
            print("❌ 잘못된 입력입니다. 1~4 사이의 숫자를 입력해 주세요.")