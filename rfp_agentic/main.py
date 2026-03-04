
from rfp_agentic.orchestrator import Orchestrator


def run() -> str:
    orchestrator = Orchestrator()
    return orchestrator.run()


if __name__ == '__main__':
    run()
