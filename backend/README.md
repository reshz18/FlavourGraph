# FlavorGraph Python Backend

## Overview

This is the Python backend for FlavorGraph: Intelligent Recipe Navigator with Algorithmic Insights. The backend implements sophisticated algorithms including Graph Theory, Backtracking, and Greedy Algorithms to provide intelligent recipe suggestions and ingredient analysis.

## 🧠 Algorithmic Features

### 1. Graph Theory Implementation
- **Ingredient Relationship Graph**: 50+ nodes, 200+ edges
- **Centrality Analysis**: Betweenness, Degree, and PageRank centrality
- **Shortest Path Analysis**: For ingredient similarity calculation
- **Graph Traversal**: For substitution finding and complementary ingredients

### 2. Backtracking Algorithm
- **Optimal Recipe Combination**: Find best recipe sets with constraints
- **Constraint Satisfaction**: Handle dietary restrictions and preferences
- **Pruning Strategies**: Bound, constraint, and dominance pruning
- **Multi-objective Optimization**: Balance variety, availability, and preferences

### 3. Greedy Algorithm
- **Fast Recipe Filtering**: O(n log n) initial candidate selection
- **Ingredient Substitution**: Locally optimal substitution selection
- **Gap Analysis**: Quick feasibility assessment for recipes

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your API keys (optional - will use mock data if not provided):
   ```env
   SPOONACULAR_API_KEY=your_api_key_here
   EDAMAM_APP_ID=your_app_id_here
   EDAMAM_APP_KEY=your_app_key_here
   ```

5. **Run the server**
   ```bash
   python run.py
   ```

The server will start on `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/api/docs
- **ReDoc Documentation**: http://localhost:8000/api/redoc

## 🔗 API Endpoints

### Core Endpoints

#### Recipe Suggestions
```http
POST /api/recipes/suggest
Content-Type: application/json

{
  "available_ingredients": ["chicken", "tomato", "onion"],
  "dietary_restrictions": ["gluten-free"],
  "cuisine_preference": "italian",
  "max_recipes": 10
}
```

#### Ingredient Gap Analysis
```http
POST /api/ingredients/gap-analysis
Content-Type: application/json

{
  "available_ingredients": ["flour", "eggs", "milk"],
  "target_recipe_id": "1"
}
```

#### Ingredient Substitutions
```http
GET /api/ingredients/substitutions/chicken?limit=5
```

#### Recipe Search
```http
GET /api/recipes/search?query=pasta&ingredients=tomato,basil&cuisine=italian&limit=20
```

#### Algorithm Demonstration
```http
GET /api/algorithms/demo
```

## 🏗️ Architecture

### Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── run.py                  # Startup script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── models/
│   └── recipe_models.py   # Pydantic data models
├── services/
│   ├── graph_service.py   # Graph theory implementation
│   ├── algorithm_service.py # Backtracking & greedy algorithms
│   └── recipe_service.py  # Recipe data management
├── utils/
│   └── logger.py          # Logging configuration
└── ALGORITHM_DOCUMENTATION.md # Detailed algorithm explanation
```

### Service Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│ Algorithm Service │────│  Graph Service  │
│   (main.py)     │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Recipe Service │    │ External APIs    │    │ NetworkX Graph  │
│                 │    │ (Spoonacular)    │    │ (Ingredients)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🧪 Algorithm Implementation Details

### Graph Theory
- **Library**: NetworkX for graph operations
- **Graph Type**: Undirected weighted graph for ingredients
- **Metrics**: Centrality measures for ingredient importance
- **Applications**: Substitution finding, similarity calculation

### Backtracking Algorithm
- **Approach**: Recursive exploration with pruning
- **Constraints**: Dietary restrictions, ingredient availability
- **Optimization**: Multi-objective scoring function
- **Pruning**: Bound, constraint, and dominance pruning

### Greedy Algorithm
- **Strategy**: Local optimization at each step
- **Applications**: Recipe filtering, substitution selection
- **Complexity**: O(n log n) for most operations
- **Benefits**: Fast execution, good approximation

## 🔧 Configuration

### Environment Variables
```env
# External API Keys (Optional)
SPOONACULAR_API_KEY=your_spoonacular_api_key
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Origins
CORS_ORIGINS=http://localhost:3000,https://your-domain.com

# Logging
LOG_LEVEL=INFO
```

### External APIs (Optional)
The backend can integrate with external recipe APIs:
- **Spoonacular API**: For extensive recipe database
- **Edamam API**: For nutrition information
- **Mock Data**: Used when API keys are not provided

## 🧪 Testing the Algorithms

### Test Recipe Suggestions
```bash
curl -X POST "http://localhost:8000/api/recipes/suggest" \
     -H "Content-Type: application/json" \
     -d '{
       "available_ingredients": ["chicken", "tomato", "onion", "garlic"],
       "dietary_restrictions": [],
       "cuisine_preference": "italian",
       "max_recipes": 5
     }'
```

### Test Ingredient Substitutions
```bash
curl "http://localhost:8000/api/ingredients/substitutions/chicken?limit=3"
```

### Test Gap Analysis
```bash
curl -X POST "http://localhost:8000/api/ingredients/gap-analysis" \
     -H "Content-Type: application/json" \
     -d '{
       "available_ingredients": ["flour", "eggs", "milk"],
       "target_recipe_id": "1"
     }'
```

### View Algorithm Demo
```bash
curl "http://localhost:8000/api/algorithms/demo"
```

## 📊 Performance Metrics

The backend tracks algorithm performance:
- **Backtracking calls**: Number of recursive operations
- **Greedy selections**: Number of greedy decisions
- **Graph traversals**: Number of graph operations
- **Execution time**: Total processing time

Access metrics via: `GET /api/algorithms/demo`

## 🔗 Frontend Integration

The backend is designed to work seamlessly with the Next.js frontend:

1. **CORS Configuration**: Allows requests from `http://localhost:3000`
2. **API Format**: Returns data in format expected by frontend components
3. **Error Handling**: Provides meaningful error messages
4. **Response Models**: Structured responses using Pydantic models

### Frontend API Integration Example
```typescript
// In your Next.js frontend
const suggestRecipes = async (ingredients: string[]) => {
  const response = await fetch('http://localhost:8000/api/recipes/suggest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      available_ingredients: ingredients,
      max_recipes: 10
    })
  });
  return response.json();
};
```

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "run.py"]
```

## 📖 Algorithm Documentation

For detailed explanation of the algorithms, see [ALGORITHM_DOCUMENTATION.md](./ALGORITHM_DOCUMENTATION.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of an academic assignment demonstrating algorithmic implementations in a practical application.

---

**FlavorGraph Backend** - Intelligent Recipe Navigation with Algorithmic Insights 🍳🧠
