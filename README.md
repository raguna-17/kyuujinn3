# 求人管理アプリ（Recruiting System）



## 概要

企業・求人・応募の採用フローを再現した採用管理システムです。

単なるCRUDアプリケーションではなく、

- roleベース認可
- 応募ステータス遷移制御
- APIレベルでの整合性保証

など、実務を意識した業務ロジックの設計・実装に重点を置いています。

本プロジェクトでは、「実務フローをどのように状態管理や認可設計へ落とし込むか」をテーマに開発しました。

特に、

- roleごとの権限制御
- ステータス遷移管理
- 業務ロジックの責務分離
- 不正状態変更の防止

を意識して設計しています。


## 🚀 Demo
## https://www.youtube.com/watch?v=DnQd_b_R2pk
## https://kyuujinn3-furonto.onrender.com


## 実装した業務フロー
* 企業の作成・管理
* 求人の作成・管理
* 求人への応募
* 応募情報の管理（企業側・応募者側）


## 🧠 業務ロジックの実装（重要ポイント）
### 応募機能（job_applications

実務を意識し、以下の制御を実装しています：

* 応募ステータス遷移制御
- roleごとのアクセス制御
+ APIレベルで不正状態変更を防止



## ステータス遷移
採用フローを状態遷移として管理しています。


```bash
VALID_TRANSITIONS = {
    "applied": ["reviewing", "rejected"],
    "reviewing": ["interview", "rejected"],
    "interview": ["accepted", "rejected"],
}
```
```bash
applied
 ├─→ reviewing
 │      ├─→ interview
 │      │      ├─→ accepted
 │      │      └─→ rejected
 │      └─→ rejected
 └─→ rejected
```

Service層で許可された遷移のみを受け付け、
不正な状態変更を防止しています。



## Authorization

Roleベース認可を実装しています。

| Role | Permissions |
|---|---|
| USER | 求人閲覧・応募 |
| COMPANY | 求人作成・応募管理 |
| ADMIN | 全権限 |

JWT認証に加え、JWT内のrole情報をそのまま信用せず、DB上のroleと照合したうえで認可を実施しています。これにより、token改ざんやrole mismatchによる不正アクセスを防止しています。

また、誰がどの応募情報を閲覧できるか、誰が応募ステータスを更新できるかをAPIレベルで制御し、roleごとのアクセス権限を管理しています。


## Architecture

ドメイン単位で責務を分割した、レイヤードアーキテクチャを採用しています。

### Domains

- users
- organizations
- job_postings
- job_applications

### Layer Structure

```text
Client
  ↓
Router
  ↓
Service
  ↓
Repository
  ↓
DB
```

- Router：HTTPリクエスト処理
- Service：業務ロジック（認可・状態遷移など）
- Repository：DBアクセス

業務ロジックをService層へ集約し、HTTP層・DBアクセス層を分離することで、保守性と責務分離を意識して設計しています。




## 💼 Frontend

featureベース構成を採用しています。

```bash
features/
 ├─ auth/
 ├─ organizations/
 ├─ job_postings/
 └─ job_applications/
```

機能単位で責務を分離し、API通信,状態管理,UI責務

を整理しています。

## 🧪 Testing

PytestによるAPIテストを実装しています。

重点的にテストした内容：

- 認可制御
- 状態遷移
- 正常系 / 異常系
- 不正状態変更
- 他ユーザーによる不正更新

業務ルールを保証するため、
正常系だけでなく異常系テストも重視しています。

## 🧪 Tech Stack
```text
Backend
FastAPI
SQLAlchemy (Async)
PostgreSQL
Alembic
Pydantic
JWT (python-jose)
Frontend
React (Vite)
JavaScript
Axios
React Router
Infrastructure
Docker
Docker Compose
```

## 🚀 Future Improvements
検索・フィルタ機能
Axios Interceptor
UI/UX改善
権限管理の拡張

## 📌 Development Focus

本プロジェクトでは、

「単純なCRUDではなく、実務フローをどう安全に管理するか」

を重視して開発しました。

特に、

状態遷移による採用フロー管理
roleベース認可
APIレベルでの整合性保証
Service層への業務ロジック集約

を意識して設計・実装しています。