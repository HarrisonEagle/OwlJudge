import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.*;
public class Main {
	public static void main(String[] args)throws IOException {
		FastReader sc = new FastReader();
		PrintWriter pw = new PrintWriter(System.out);
		int n = sc.nextInt();
		int m = sc.nextInt();
		ArrayList<ArrayList<Edge>> graph = new ArrayList<>();
		for (int i = 0; i < n + 1; i++) {
			graph.add(new ArrayList<>());
		}
		for (int i = 0; i < m; i++) {
			int src = sc.nextInt();
			int dest = sc.nextInt();
			int len = 1;
			graph.get(src).add(new Edge(dest, len));
			graph.get(dest).add(new Edge(src, len));
		}
		djikstra(graph, n);


	}
	public static void djikstra(ArrayList<ArrayList<Edge>> graph, int n) {
		int distance[] = new int[n + 1];
		Arrays.fill(distance, Integer.MAX_VALUE);
		distance[1] = 0;
		PriorityQueue<Edge> pq = new PriorityQueue<>(new Edge());
		pq.add(new Edge(1, 1));
		HashSet<Integer> set = new HashSet<>();
		HashMap<Integer, Integer> map = new HashMap<>();
		while (!pq.isEmpty()) {
			int minVertex = pq.poll().src;
			set.add(minVertex);
			for (int i = 0; i < graph.get(minVertex).size(); i++) {
				Edge curr = graph.get(minVertex).get(i);
				if (!set.contains(curr.src)) {
					int currdist = distance[minVertex] + curr.len;
					if (currdist < distance[curr.src]) {
						distance[curr.src] = currdist;
						pq.add(new Edge(curr.src, currdist));
						map.put(curr.src, minVertex);
					}
				}
			}

		}
		for (int i = 1; i <= n; i++) {
			if (distance[i] == Integer.MAX_VALUE) {
				System.out.println("No"); return;
			}
		}
		System.out.println("Yes");
		for (int i = 2; i <= n; i++) {
			System.out.println(map.get(i));
		}
	}
}

class Edge implements Comparator<Edge> {
	int src, len;
	public Edge()
	{}
	public Edge(int a, int b) {
		src = a;
		len = b;
	}
	public int compare(Edge e1, Edge e2) {
		if (e1.len > e2.len)
			return 1;
		return -1;
	}
}



class FastReader {
	BufferedReader br;
	StringTokenizer st;

	public FastReader() {
		br = new BufferedReader(new
		                        InputStreamReader(System.in));
	}

	String next() {
		while (st == null || !st.hasMoreElements()) {
			try {
				st = new StringTokenizer(br.readLine());
			} catch (IOException  e) {
				e.printStackTrace();
			}
		}
		return st.nextToken();
	}

	int nextInt() {
		return Integer.parseInt(next());
	}

	long nextLong() {
		return Long.parseLong(next());
	}

	double nextDouble() {
		return Double.parseDouble(next());
	}

	String nextLine() {
		String str = "";
		try {
			str = br.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return str;
	}
}
