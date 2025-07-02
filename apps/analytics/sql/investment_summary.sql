CREATE OR REPLACE VIEW investment_summary AS
SELECT
  user_id,
  COUNT(*) AS investment_count,
  SUM(amount_invested) AS total_invested,
  SUM(current_value) AS total_value
FROM
  investments_userinvestment
GROUP BY user_id;
