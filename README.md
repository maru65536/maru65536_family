# maru65536_family

### 実行

必要なライブラリをインストールして、起動します
```bash
docker-compose build
docker-compose up -d
```

### テーブルの作成

起動しているコンテナに入ります。

```bash
docker-compose exec db mysql -u root -p
```

ファイルからSQLを実行します

```sql
source /sql/000_initialize_tables.sql
```

### flaskのログを見る

実行中のコンテナにattachします
```bash
docker attach maru65536_family_app_1
```