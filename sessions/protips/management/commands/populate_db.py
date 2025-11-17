from django.core.management.base import BaseCommand
from django.db import transaction
from protips.models import CustomUser, Tip, Vote


class Command(BaseCommand):
	help = 'Populate database with 30 users and specific tips with votes'

	def handle(self, *args, **options):
		self.stdout.write(self.style.WARNING('Starting database population...'))

		with transaction.atomic():
			# * Create 31 users (30 main + 1 extra for 30 votes on user_2's tip)
			users = []
			for i in range(1, 32):
				username = f'user_{i}'
				user, created = CustomUser.objects.get_or_create(
					username=username,
					defaults={
						'email': f'{username}@example.com',
						'first_name': f'User',
						'last_name': f'{i}',
					}
				)
				if created:
					user.set_password('password123')
					user.save()
					self.stdout.write(self.style.SUCCESS(f'✓ Created user: {username}'))
				else:
					self.stdout.write(f'  User {username} already exists')
				users.append(user)

			# * Create tip for user_1 with 15 upvotes
			user_1 = users[0]
			tip_1_content = """
			Pro Tip #1: Always write clean and maintainable code!
			"""
			tip_1, created = Tip.objects.get_or_create(
				author=user_1,
				defaults={'content': tip_1_content.strip()}
			)
			if created:
				self.stdout.write(self.style.SUCCESS(f'✓ Created tip for user_1'))
			else:
				self.stdout.write(f'  Tip for user_1 already exists')

			# ! Add 15 upvotes to tip_1
			upvote_count = 0
			for i in range(15):
				voter = users[i + 1]  # user_2 to user_16
				vote, created = Vote.objects.get_or_create(
					tip=tip_1,
					user=voter,
					defaults={'value': Vote.UPVOTE}
				)
				if created:
					upvote_count += 1

			self.stdout.write(self.style.SUCCESS(f'✓ Added {upvote_count} upvotes to tip_1 (Reputation: {user_1.calculate_reputation()})'))

			# * Create tip for user_2 with 30 upvotes
			user_2 = users[1]
			tip_2_content = """
			Pro Tip #2: Master Django best practices!
			"""
			tip_2, created = Tip.objects.get_or_create(
				author=user_2,
				defaults={'content': tip_2_content.strip()}
			)
			if created:
				self.stdout.write(self.style.SUCCESS(f'✓ Created tip for user_2'))
			else:
				self.stdout.write(f'  Tip for user_2 already exists')

			# ! Add 30 upvotes to tip_2 (but we only have 30 users total)
			# ! user_2 is the author, so we use the other 29 users
			upvote_count_2 = 0
			for i, user in enumerate(users):
				if user != user_2:  # Skip the author
					vote, created = Vote.objects.get_or_create(
						tip=tip_2,
						user=user,
						defaults={'value': Vote.UPVOTE}
					)
					if created:
						upvote_count_2 += 1
					
					if upvote_count_2 >= 30:
						break

			self.stdout.write(self.style.SUCCESS(f'✓ Added {upvote_count_2} upvotes to tip_2 (Reputation: {user_2.calculate_reputation()})'))

			# * Summary
			self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
			self.stdout.write(self.style.SUCCESS('Database population completed!'))
			self.stdout.write(self.style.SUCCESS('=' * 50))
			self.stdout.write(f'Total users created: 31 (30 main + 1 extra voter)')
			self.stdout.write(f'user_1 tip upvotes: 15 (Reputation: {user_1.calculate_reputation()})')
			self.stdout.write(f'user_2 tip upvotes: {upvote_count_2} (Reputation: {user_2.calculate_reputation()})')
			self.stdout.write(self.style.SUCCESS('=' * 50))
			self.stdout.write(self.style.WARNING('\nLogin credentials for all users:'))
			self.stdout.write('  Username: user_1 to user_31')
			self.stdout.write('  Password: password123')
