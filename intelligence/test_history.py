
from intelligence.cleaning_history import CleaningHistory

history = CleaningHistory()

history.record_cleaning(0, 0, 2)
history.record_cleaning(1, 2, 3)
history.record_cleaning(3, 4, 1)

history.show_history()

print("\nTotal dirt cleaned:", history.total_dirt_cleaned())
