# Security Update Summary - 評分邏輯完全保護

## 🔐 重要修改說明

為了防止學生竄改評分邏輯和 exit code，已將**所有**評分相關邏輯移至受保護的檔案中。

---

## 📂 檔案結構（更新後）

### ✅ 學生可編輯的檔案（Student Files）
這些檔案學生可以修改，但**不包含任何評分邏輯**：

```
Markowitz.py          # 學生只需填寫 3 個 TODO 區塊
Markowitz_2.py        # 學生只需填寫 1 個 TODO 區塊
```

**學生檔案內容**：
- ✅ 資料處理邏輯
- ✅ 類別定義（Portfolio 類別）
- ✅ TODO 區塊（學生需實作的部分）
- ✅ argparse 參數定義
- ❌ **沒有任何評分邏輯**
- ❌ **沒有 exit code 判斷**
- ❌ **沒有分數計算**

### 🔒 受保護的評分檔案（Protected Grading Files）
這些檔案**必須**在 GitHub Classroom 設為 Protected：

```
grader.py             # Markowitz.py 的評分系統
grader_2.py           # Markowitz_2.py 的評分系統
.github/workflows/classroom.yml
Answer/**
```

**評分檔案內容**：
- ✅ Helper 類別（視覺化工具）
- ✅ AssignmentJudge 類別（評分邏輯）
- ✅ `run_grading(args)` 方法（包含所有 if/else 邏輯）
- ✅ **Exit code 判斷**（sys.exit(0/1)）
- ✅ **分數計算與比對**
- ✅ **所有測試邏輯**

---

## 🔄 程式執行流程

### Markowitz.py 執行流程
```python
# 1. 學生檔案 (Markowitz.py) - 可編輯但無危險邏輯
if __name__ == "__main__":
    from grader import AssignmentJudge  # ← 從受保護檔案匯入
    
    parser = argparse.ArgumentParser(...)
    parser.add_argument("--score", ...)
    parser.add_argument("--allocation", ...)
    # ... 其他參數定義
    
    args = parser.parse_args()
    judge = AssignmentJudge()
    
    # ⚠️ 所有邏輯都在受保護的 grader.py 中執行
    judge.run_grading(args)  # ← 呼叫受保護的方法
```

```python
# 2. 受保護檔案 (grader.py) - 學生無法修改
class AssignmentJudge:
    def run_grading(self, args):
        """所有評分邏輯都在這裡（受保護）"""
        if args.score:
            if ("eqw" in args.score) or ("rp" in args.score) or ("mv" in args.score):
                # 本機測試個別題目
                if "eqw" in args.score:
                    self.check_answer_eqw(self.eqw)
                # ...
                
            elif "all" in args.score:
                # GitHub Classroom autograding
                total_score = self.check_all_answer()
                print(f"==> total Score = {total_score} <==")
                
                # ⚠️ Exit code 邏輯（學生無法竄改）
                FULL_SCORE = 70
                if total_score == FULL_SCORE:
                    sys.exit(0)  # ✅ 全對 → 70/70
                else:
                    sys.exit(1)  # ❌ 有錯 → 0/70
        
        if args.allocation:
            # 視覺化邏輯...
        
        if args.performance:
            # 效能檢查邏輯...
        
        if args.report:
            # 報告邏輯...
```

### Markowitz_2.py 執行流程
```python
# 1. 學生檔案 (Markowitz_2.py) - 相同架構
if __name__ == "__main__":
    from grader_2 import AssignmentJudge
    
    parser = argparse.ArgumentParser(...)
    # ... 參數定義
    
    args = parser.parse_args()
    judge = AssignmentJudge()
    
    judge.run_grading(args)  # ← 所有邏輯在 grader_2.py
```

```python
# 2. 受保護檔案 (grader_2.py)
class AssignmentJudge:
    def run_grading(self, args):
        """所有評分邏輯都在這裡（受保護）"""
        if args.score:
            # ...
            elif "all" in args.score:
                total_score = self.check_all_answer()
                print(f"==> total Score = {total_score} <==")
                
                FULL_SCORE = 30
                if total_score == FULL_SCORE:
                    sys.exit(0)  # ✅ 全對 → 30/30
                else:
                    sys.exit(1)  # ❌ 有錯 → 0/30
        # ...
```

---

## 🛡️ 安全性檢查清單

### ✅ 已防護的攻擊向量

- [x] **無法竄改評分邏輯** - 所有 `check_answer_*` 方法在受保護檔案
- [x] **無法修改 exit code** - `sys.exit(0/1)` 邏輯在受保護檔案
- [x] **無法修改滿分設定** - `FULL_SCORE` 常數在受保護檔案
- [x] **無法繞過測試** - 整個 `run_grading()` 方法受保護
- [x] **無法修改標準答案** - `Answer/` 資料夾受保護
- [x] **無法修改 workflow** - `.github/workflows/classroom.yml` 受保護

### ❌ 學生無法做的事情

```python
# 學生想作弊但做不到的例子：

# ❌ 無法這樣改 (因為邏輯在 grader.py，檔案受保護)
if total_score >= 0:  # 改成永遠 True
    sys.exit(0)

# ❌ 無法這樣改 (因為 run_grading 在受保護檔案)
def run_grading(self, args):
    sys.exit(0)  # 直接返回成功

# ❌ 無法這樣改 (因為 check_all_answer 在受保護檔案)
def check_all_answer(self):
    return 70  # 直接返回滿分

# ❌ 無法這樣改 (因為 FULL_SCORE 在受保護檔案)
FULL_SCORE = 0  # 改成 0 讓任何分數都算滿分
```

---

## 🔒 GitHub Classroom Protected Paths 設定

**必須設定以下 Protected paths**（重要！）：

```
grader.py
grader_2.py
.github/workflows/classroom.yml
Answer/**
```

### 設定步驟：
1. 進入 GitHub Classroom → 選擇 Assignment
2. 點擊 **Settings** 或 **Edit assignment**
3. 找到 **Protected paths** 區塊
4. 加入上述 4 個路徑
5. **Save** 儲存

---

## 📊 評分架構

### Markowitz.py (70分)
- Problem 1 (EQW): 20分
- Problem 2 (RP): 20分  
- Problem 3 (MV): 30分

**評分邏輯**：`grader.py` 的 `run_grading()` 方法
- 全對 (70分) → `sys.exit(0)` → GitHub Actions 給 70/70
- 有錯 (0-69分) → `sys.exit(1)` → GitHub Actions 給 0/70

### Markowitz_2.py (30分)
- Problem 4.1 (Sharpe > 1): 15分
- Problem 4.2 (Sharpe > SPY): 15分

**評分邏輯**：`grader_2.py` 的 `run_grading()` 方法
- 全對 (30分) → `sys.exit(0)` → GitHub Actions 給 30/30
- 有錯 (0-29分) → `sys.exit(1)` → GitHub Actions 給 0/30

**總分：100分**

---

## 🧪 測試指令

### 本機測試（教師/學生用）
```bash
# 測試個別題目（不會 exit）
python Markowitz.py --score eqw
python Markowitz.py --score rp
python Markowitz.py --score mv

# 測試全部（會根據結果 exit）
python Markowitz.py --score all
python Markowitz_2.py --score all

# 視覺化
python Markowitz.py --allocation eqw
python Markowitz.py --performance mv
python Markowitz.py --report mv
```

### GitHub Actions 自動測試
```yaml
# .github/workflows/classroom.yml
- name: Run Markowitz Test
  command: python Markowitz.py --score all
  max-score: 70

- name: Run Markowitz 2 Test  
  command: python Markowitz_2.py --score all
  max-score: 30
```

---

## ✨ 改進優點

### Before（舊版，不安全）
```python
# Markowitz.py - 學生可編輯
if args.score:
    if "all" in args.score:
        total_score = judge.check_all_answer()
        FULL_SCORE = 70
        if total_score == FULL_SCORE:
            sys.exit(0)  # ⚠️ 學生可以改成 sys.exit(0) 作弊
        else:
            sys.exit(1)
```

### After（新版，安全）
```python
# Markowitz.py - 學生可編輯但無危險邏輯
if __name__ == "__main__":
    from grader import AssignmentJudge
    args = parser.parse_args()
    judge = AssignmentJudge()
    judge.run_grading(args)  # ✅ 所有邏輯在受保護檔案

# grader.py - 受保護，學生無法修改
class AssignmentJudge:
    def run_grading(self, args):
        if args.score and "all" in args.score:
            total_score = self.check_all_answer()
            FULL_SCORE = 70
            if total_score == FULL_SCORE:
                sys.exit(0)  # ✅ 學生無法修改此檔案
            else:
                sys.exit(1)
```

---

## ⚠️ 重要提醒

1. **必須設定 Protected Paths**  
   否則學生可以修改 `grader.py` 和 `grader_2.py`

2. **測試 Protected Paths 是否生效**  
   建立一個測試學生帳號，嘗試修改受保護檔案，應該會被拒絕

3. **更新標準答案**  
   需從教師的 template repository 修改，不能在學生 repo 中修改

4. **確認 workflow 正常運作**  
   Push 測試看 GitHub Actions 是否正確執行

---

## 🎯 結論

現在的架構下：
- ✅ 學生**只能**修改他們的作業邏輯（TODO 區塊）
- ✅ 學生**無法**修改評分邏輯
- ✅ 學生**無法**竄改 exit code
- ✅ 學生**無法**修改分數計算
- ✅ 評分系統**完全受保護**

**設定 Protected Paths 後即可安全發布作業！** 🎉
