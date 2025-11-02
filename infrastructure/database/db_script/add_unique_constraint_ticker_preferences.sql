-- Añade un constraint único para evitar duplicados en ticker_preferences
ALTER TABLE public.ticker_preferences
ADD CONSTRAINT unique_user_ticker_drop_days
UNIQUE (user_id, ticker, drop_percentage, days);

