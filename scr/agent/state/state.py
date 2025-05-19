from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any
from langgraph.managed import IsLastStep
from langchain_core.documents import Document
from typing import Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BeforeValidator
import json
import ast


class StepOutput(BaseModel):
    """Represents a step the agent went through to generate the answer."""

    label: str
    """The human-readable title for this step to be displayed to the user."""

    details: str = Field(default="")
    """Details of the steps results in markdown to be displayed to the user. It can be either a markdown string or a list of StepOutput."""

    substeps: Optional[List["StepOutput"]] = Field(default_factory=list)
    """Optional substeps for a step."""

    type: Literal["context", "fix-message", "recall"] = Field(default="context")
    """The type of the step."""

    fixed_message: Optional[str] = None
    """The fixed message to replace the last message sent to the user."""


class StructuredQuestion(BaseModel):
    """Structured informations extracted from the user question."""

    # intent: Literal["general_information", "access_resources"] = Field(
    #     default="access_resources",
    #     description="Intent extracted from the user question",
    # )
    extracted_classes: List[str] = Field(
        default_factory=list,
        description="List of classes extracted from the user question",
    )
    extracted_entities: List[str] = Field(
        default_factory=list,
        description="List of entities extracted from the user question",
    )
    question_steps: List[str] = Field(
        default_factory=list,
        description="List of steps extracted from the user question",
    )


class Candidate(BaseModel):
    pattern: str = Field(default="")

class BlockState(BaseModel):
    endpoint: str = Field(default="")
    iri_map: Dict[str, str] = Field(default_factory=dict)
    validated_pattern: str = Field(default="")
    failed_patterns: List[Dict[str, str]] = Field(default_factory=lambda: [])
    attempt: int = Field(default=1)
    final: bool = Field(default=False)
    target_endpoint: str = Field(default="")

def parse_string_to_dict(v: Any) -> dict:
    """Parse a string to a dictionary if it's a string."""
    if isinstance(v, str):
        try:
             return ast.literal_eval(v)
        except (SyntaxError, ValueError):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON string: {v}")
    return v

class QueryPlan(BaseModel):

    iri_map: Annotated[Dict[str, str], BeforeValidator(parse_string_to_dict)] = Field(default_factory=dict)
    """Mapping of entities identified in user question to ontology IRIs from provided context (or own knowledge)."""

    early_select: List[str] = Field(default_factory=list)
    """List of early select variables (early draft SELECT)."""

    federated_endpoints: List[str] = Field(default_factory=list)
    """List of endpoints that are used in the query."""
    target_endpoint: str = Field(default="")
    """Target endpoint where the final query is executed."""

class QueryState(BaseModel):
    question: str = Field(default="")
    blocks: List[BlockState] = Field(default_factory=list)
    global_iri_map: Dict[str, str] = Field(default_factory=dict)
    joins: Dict[str, str] = Field(default_factory=dict)
    final_query: str = Field(default="")
    query_plan: QueryPlan = Field(default_factory=QueryPlan)
    done: bool = Field(default=False)


@dataclass
class BaseState:
    """Base state with messages field."""
    messages: Annotated[List[BaseMessage], add_messages]


@dataclass
class State(BaseState):
    """Represents the complete state of the agent, extending InputState with additional attributes.

    This class can be used to store any information needed throughout the agent's lifecycle.
    """

    is_last_step: IsLastStep = field(default=False)
    """Indicates whether the current step is the last one before the graph raises an error.

    This is a 'managed' variable, controlled by the state machine rather than user code.
    It is set to 'True' when the step count reaches recursion_limit - 1.
    """

    structured_question: StructuredQuestion = field(default_factory=StructuredQuestion)
    """Structured information extracted from the user's question."""

    #retrieved_docs: List[Document] = field(default_factory=list)
    """Documents retrieved from the knowledge base."""

    extracted_entities: List[str] = field(default_factory=list)
    """List of entities extracted and resolved from the question."""

    extracted_classes: List[str] = field(default_factory=list)
    """List of classes extracted from the question."""

    extracted_example_queries: List[str] = field(default_factory=list)
    """List of example queries extracted from the question."""

    query_state: QueryState = field(default_factory=QueryState)
    """The query state."""

    structured_output: str = field(default="")
    """The final structured output (e.g., SPARQL query)."""

    steps: List[StepOutput] = field(default_factory=list)
    """List of steps taken during the agent's execution."""
