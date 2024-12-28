from crew_ai import Agent

##############################################################
# Agent: Planner
#
##############################################################
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
    "about the topic: {topic}."
    "You collect information that helps the "
    "audience learn something "
    "and make informed decisions. "
    "Your work is the basis for "
    "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    tools=[scrape_tool, search_tool],
)

##############################################################
# Agent: Researcher
#
##############################################################
researcher = Agent(
    role="Tech Researcher",
    goal="To find excellent sources of information for the writer to use as a starting point.",
    tools=[search_tool, scrape_tool, codeDocTool, youtubeChannelTool, youtubeVideoTool],
    backstory=(
        "As a Tech Researcher, your prowess in "
        "navigating and extracting critical "
        "information from documentation is unmatched."
        "You are an expert in reading code and translating it to plain english"
    ),
)
##############################################################
# Agent: Writer
#
##############################################################
writer = Agent(
    role="Content Writer",
    goal="Write insightful and easy to follow " "tutorial about the topic: {topic}",
    backstory="You're working on a writing "
    "a new tutorial about the topic: {topic}. "
    "You base your writing on the work of "
    "the Content Planner, who provides an outline "
    "and relevant context about the topic. "
    "You follow the main objectives and "
    "direction of the outline, "
    "as provide by the Content Planner. "
    "You also provide objective and impartial insights "
    "and back them up with information "
    "provide by the Content Planner. "
    "You state your sources.",
    allow_delegation=False,
)

##############################################################
# Agent: Editor
#
##############################################################
editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
    "the writing style of the organization. "
    "Ensure that the blog post is written for beginners",
    backstory="You are an editor who receives a blog post "
    "from the Content Writer. "
    "Your goal is to review the blog post "
    "to ensure that it follows journalistic best practices,"
    "provides balanced viewpoints "
    "when providing opinions or assertions, "
    "and also avoids major controversial topics "
    "or opinions when possible.",
    allow_delegation=False,
)
