from intelligence.knowledge_base import KnowledgeBase

# Create a 5x5 knowledge base
memory = KnowledgeBase(5, 5)

# Robot explores some cells
memory.update_cell(0, 0, 2)
memory.update_cell(0, 1, 0)
memory.update_cell(1, 1, 3)
memory.update_cell(2, 2, 0, obstacle=True)

# Display knowledge
print("Before cleaning:")
memory.display_knowledge()

# Robot cleans cell (0,0)
memory.mark_cleaned(0, 0)

# Display updated knowledge
print("\nAfter cleaning:")
memory.display_knowledge()

# Check visit count
print("\nVisits to cell (0,0):",
      memory.get_visits(0, 0))
