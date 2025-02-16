import subprocess
import sys
from collections import Counter
import re

def analyze_game_output(output):
    """Analyze the game output to understand what happened"""
    analysis = {
        'moves': [],
        'final_board': '',
        'error': None,
        'winner': None,
        'game_length': 0,
        'piece_counts': {'initial': {'white': 0, 'black': 0}, 
                        'final': {'white': 0, 'black': 0}}
    }
    
    # Split output into board states
    board_states = output.split('----------------------')
    
    # Count initial pieces
    if len(board_states) > 1:
        first_board = board_states[0]
        analysis['piece_counts']['initial']['white'] = first_board.count('w')
        analysis['piece_counts']['initial']['black'] = first_board.count('b')
        
        # Count final pieces
        last_board = board_states[-2] if len(board_states) > 2 else board_states[-1]
        analysis['piece_counts']['final']['white'] = last_board.count('w')
        analysis['piece_counts']['final']['black'] = last_board.count('b')
        
        analysis['final_board'] = last_board
        analysis['game_length'] = len(board_states) - 1
    
    # Check for crashes or errors
    if "crashed" in output.lower():
        analysis['error'] = "AI Crashed"
    elif "invalid move" in output.lower():
        analysis['error'] = "Invalid Move"
    
    # Determine winner
    if "player 1 wins" in output.lower():
        analysis['winner'] = 1
    elif "player 2 wins" in output.lower():
        analysis['winner'] = 2
    elif "tie" in output.lower():
        analysis['winner'] = 0
        
    return analysis

def run_single_game():
    try:
        result = subprocess.run([
            'python3', 'AI_Runner.py', '7', '7', '2', 'l',
            '../src/checkers-python/main.py',
            'Sample_AIs/Random_AI/main.py'
        ], capture_output=True, text=True, timeout=30)
        
        return result.stdout, analyze_game_output(result.stdout)
        
    except subprocess.TimeoutExpired:
        return None, {'error': 'Timeout', 'winner': None}
    except Exception as e:
        return None, {'error': str(e), 'winner': None}

def run_games(num_games=100):
    results = []
    game_analyses = []
    timeouts = 0
    crashes = 0
    invalid_moves = 0
    
    print("\nStarting games...\n")
    
    for game in range(num_games):
        print(f"\rPlaying game {game + 1}/{num_games}...", end="", flush=True)
        
        output, analysis = run_single_game()
        
        if analysis['winner'] is not None:
            results.append(analysis['winner'])
            game_analyses.append(analysis)
            
            # Track problems
            if analysis.get('error') == "AI Crashed":
                crashes += 1
            elif analysis.get('error') == "Invalid Move":
                invalid_moves += 1
        else:
            timeouts += 1
            
    print("\n\nDetailed Analysis:")
    print("=================")
    
    total_games = len(results)
    if total_games == 0:
        print("No games were successfully completed.")
        return 0
        
    counts = Counter(results)
    wins = counts[1]
    losses = counts[2]
    ties = counts[0]
    
    print(f"\nOverall Results:")
    print(f"Total games completed: {total_games}")
    print(f"Games timed out: {timeouts}")
    print(f"AI crashes: {crashes}")
    print(f"Invalid moves: {invalid_moves}")
    print(f"Wins: {wins} ({(wins/total_games)*100:.2f}%)")
    print(f"Losses: {losses} ({(losses/total_games)*100:.2f}%)")
    print(f"Ties: {ties} ({(ties/total_games)*100:.2f}%)")
    
    # Analyze game patterns
    total_moves = sum(a['game_length'] for a in game_analyses)
    avg_game_length = total_moves / len(game_analyses) if game_analyses else 0
    
    print(f"\nGame Statistics:")
    print(f"Average game length: {avg_game_length:.1f} moves")
    
    # Analyze piece losses
    piece_losses = []
    for analysis in game_analyses:
        initial = analysis['piece_counts']['initial']
        final = analysis['piece_counts']['final']
        if analysis['winner'] == 2:  # In losses
            piece_loss = initial['white'] - final['white']
            piece_losses.append(piece_loss)
    
    if piece_losses:
        avg_piece_loss = sum(piece_losses) / len(piece_losses)
        print(f"Average piece loss in defeats: {avg_piece_loss:.1f} pieces")
    
    # Common failure patterns
    if losses > 0:
        print("\nCommon Loss Patterns:")
        early_losses = sum(1 for a in game_analyses 
                         if a['winner'] == 2 and a['game_length'] < 10)
        if early_losses:
            print(f"- Early game losses (< 10 moves): {early_losses}")
        
        piece_heavy_losses = sum(1 for a in game_analyses 
                               if a['winner'] == 2 and 
                               (a['piece_counts']['initial']['white'] - 
                                a['piece_counts']['final']['white'] > 3))
        if piece_heavy_losses:
            print(f"- Heavy piece losses (> 3 pieces): {piece_heavy_losses}")
    
    return wins/total_games * 100 if total_games > 0 else 0

if __name__ == "__main__":
    try:
        num_games = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        win_rate = run_games(num_games)
        if win_rate >= 60:
            print("\nSuccess! AI beats the 60% win rate requirement!")
        else:
            print("\nAI needs improvement to reach 60% win rate.")
    except KeyboardInterrupt:
        print("\nTesting interrupted")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")