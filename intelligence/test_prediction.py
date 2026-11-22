
from intelligence.dust_prediction import DustPrediction

prediction = DustPrediction(5, 5)

# Simulate dirt appearing in different cells
prediction.record_dirt(0, 0)
prediction.record_dirt(0, 0)
prediction.record_dirt(1, 2)
prediction.record_dirt(0, 0)

# Simulate cleaning those cells
prediction.record_cleaning(0, 0)
prediction.record_cleaning(0, 0)
prediction.record_cleaning(1, 2)

prediction.display_predictions()

print("\nPrediction for cell (0,0):",
      prediction.predict_dirt(0, 0))
