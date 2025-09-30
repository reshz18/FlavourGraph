CREATE TABLE IF NOT EXISTS recipes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  name TEXT NOT NULL,
  description TEXT,
  ingredients JSONB NOT NULL,
  instructions TEXT NOT NULL,
  prep_time TEXT,
  cook_time TEXT,
  servings INTEGER,
  image_url TEXT
);
